import os
import sys
import locale
import zipfile
import numpy as np
import pandas as pd

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

lista_regioes = [
    "n1/all",
    "n7/1501",
    "n7/2301",
    "n7/2601",
    "n7/2901",
    "n7/3101",
    "n7/3201",
    "n7/3301",
    "n7/3501",
    "n7/4101",
    "n7/4301",
]


def processa_ipca(regiao):
    ipca_detalhado = pd.read_csv(
        f"https://sidra.ibge.gov.br/geratabela?format=us.csv&name=tabela7060.csv&terr=N&rank=-&query=t/7060/{regiao}/v/all/p/all/c315/all/d/v63%202,v66%204,v69%202,v2265%202/l/,,c315%2Bp%2Bv%2Bt",
        skiprows=1,
    )
    filtro = ipca_detalhado["Mês"].str.contains(pat="[0-9]{4}", regex=True)
    filtro = filtro.fillna(False)
    ipca_detalhado = ipca_detalhado[filtro].copy()
    ipca_detalhado["Mês"] = ipca_detalhado["Mês"].apply(
        lambda x: pd.to_datetime(x, format="%B %Y")
    )
    ipca_detalhado.columns = ["categoria", "data", "variavel", "regiao", "valor"]

    ipca_detalhado[["codigo", "categoria"]] = ipca_detalhado["categoria"].str.split(
        ".", n=1, expand=True
    )
    ipca_detalhado["categoria"].fillna("Índice geral", inplace=True)
    ipca_detalhado["agrupamento"] = np.select(
        [
            ipca_detalhado["codigo"].str.len() == 1,
            ipca_detalhado["codigo"].str.len() == 2,
            ipca_detalhado["codigo"].str.len() == 4,
            ipca_detalhado["codigo"].str.len() == 7,
        ],
        ["grupo", "subgrupo", "item", "subitem"],
        default="Índice geral",
    )

    ipca_detalhado = ipca_detalhado[
        ["codigo", "agrupamento", "categoria", "data", "variavel", "regiao", "valor"]
    ]

    return ipca_detalhado


ipca = [processa_ipca(regiao) for regiao in lista_regioes]
ipca = pd.concat(ipca)

# IPCA série histórica
ipca_serie = pd.read_csv(
    "https://sidra.ibge.gov.br/geratabela?format=us.csv&name=tabela1737.csv&terr=N&rank=-&query=t/1737/n1/all/v/63,69,2265/p/all/d/v63%202,v69%202,v2265%202/l/,,t%2Bv%2Bp",
    skiprows=1,
)
filtro = ipca_serie["Mês"].str.contains(pat="[0-9]{4}", regex=True)
filtro = filtro.fillna(False)
ipca_serie = ipca_serie[filtro].copy()
ipca_serie["Mês"] = ipca_serie["Mês"].apply(lambda x: pd.to_datetime(x, format="%B %Y"))
ipca_serie.columns = ["regiao", "variavel", "data", "valor"]
ipca_serie = ipca_serie[ipca_serie["data"] >= "2002-01-01"]

# IPCA por grupo a partir de 2020
ipca_grupo = ipca[ipca["agrupamento"] == "grupo"]

# Ipca por subitem no último período
ipca_subitem = ipca[ipca["agrupamento"] == "subitem"]
ipca_subitem = ipca_subitem[ipca_subitem["data"] == ipca_subitem["data"].max()]

sys.stdout.reconfigure(encoding="utf-8")
with zipfile.ZipFile("ipca.zip", "w") as myzip:
    myzip.writestr("ipca_serie.csv", ipca_serie.to_csv(index=False, encoding="utf-8"))
    myzip.writestr("ipca_grupo.csv", ipca_grupo.to_csv(index=False, encoding="utf-8"))
    myzip.writestr(
        "ipca_subitem.csv", ipca_subitem.to_csv(index=False, encoding="utf-8")
    )

with open("ipca.zip", "rb") as f:
    sys.stdout.buffer.write(f.read())

os.remove("ipca.zip")
