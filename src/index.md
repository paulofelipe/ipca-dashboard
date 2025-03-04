---
toc: false
theme: [wide, air, alt]
# footer: "© 2024. Todos os direitos reservados."
---

```js
import {locale, number_locale} from "./components/locale.js";
```

<h1>IPCA</h1>
<h2>Dashboard com informações detalhadas do Índice de Preços ao Consumidor Amplo (IPCA)</h2>
<p>Os dados utilizados neste dashboard são originários do sistema SIDRA do IBGE e estão disponíveis para download <a href="https://sidra.ibge.gov.br/pesquisa/snipc/ipca/tabelas">aqui</a>.</p>

```js
const ipca_zip = FileAttachment("data/ipca.zip").zip();
let ipca_serie = await ipca_zip.then((zip) => zip.file("ipca_serie.csv").csv({ typed: true }));
ipca_serie.map(
  d => {
    d.ano = +d3.utcFormat("%Y")(d.data);
    d.mes = d3.utcFormat("%B")(d.data);
  }
)

let ipca_grupo = await ipca_zip.then((zip) => zip.file("ipca_grupo.csv").csv({ typed: true }));
ipca_grupo.map(
  d => {
    d.ano = +d3.utcFormat("%Y")(d.data);
    d.mes = d3.utcFormat("%B")(d.data);
  }
)

let ipca_subitem = await ipca_zip.then((zip) => zip.file("ipca_subitem.csv").csv({ typed: true }));
ipca_subitem.map(
  d => {
    d.ano = +d3.utcFormat("%Y")(d.data);
    d.mes = d3.utcFormat("%B")(d.data);
  }
)
```

```js
const data_max = d3.max(await ipca_serie, d => d.data)
const data_min = d3.utcMonth.offset(data_max, -11)
const ano_atual = d3.utcFormat("%Y")(data_max)
const mes_atual = d3.utcFormat("%B")(data_max)

const var_mensal = aq.from(ipca_serie)
  .filter(d => d.variavel == "IPCA - Variação mensal (%)")
  .filter(aq.escape(d => d.data == data_max))
  .objects()

const var_acum_ano = aq.from(ipca_serie)
  .filter(d => d.variavel == "IPCA - Variação acumulada no ano (%)")
  .filter(d => d.data == aq.op.max(d.data))
  .objects()

const var_acum_12m = aq.from(ipca_serie)
  .filter(d => d.variavel == "IPCA - Variação acumulada em 12 meses (%)")
  .filter(d => d.data == aq.op.max(d.data))
  .objects()
```

```js
const series = [
  "IPCA - Variação mensal (%)",
  "IPCA - Variação acumulada no ano (%)",
  "IPCA - Variação acumulada em 12 meses (%)"
]
```

<div class="grid grid-cols-3">
  <div class="card">
    <h2>Variação mensal</h2>
    <h1>${number_locale.format(".2%")(var_mensal[0]["valor"] / 100)}</h1>
    <h3>${d3.utcFormat("%B/%Y")(data_max)}</h3>
  </div>
  <div class="card">
    <h2>Variação acumulada no ano</h2>
    <h1>${number_locale.format(".2%")(var_acum_ano[0]["valor"] / 100)}</h1>
    <h3>Janeiro a ${d3.utcFormat("%B/%Y")(data_max)}</h3>
  </div>
  <div class="card">
    <h2>Variação acumulada em 12 meses</h2>
    <h1>${number_locale.format(".2%")(var_acum_12m[0]["valor"] / 100)}</h1>
    <h3>${d3.utcFormat("%B/%Y")(data_min)} a ${d3.utcFormat("%B/%Y")(data_max)}</h3>
  </div>
</div>


```js
const input_serie = Inputs.select(
  series, {
    label: "Série",
    format: x => x.slice(7),
    value: series[0],
    width: 360
  });
const serie = Generators.input(input_serie);
```

```js
const comparacao_mes = aq.from(ipca_serie)
  .filter(d => d.variavel == "IPCA - Variação mensal (%)")
  .filter(aq.escape(d => d.mes == mes_atual))
  .objects()

const comparacao_acum = aq.from(ipca_serie)
  .filter(d => d.variavel == "IPCA - Variação acumulada no ano (%)")
  .filter(aq.escape(d => d.mes == mes_atual))
  .objects()
```

```js
function plot_serie(width, serie) {
  const data_plot = ipca_serie.filter(d => d.variavel == serie);
  const height = 250;
  const plot = Plot.plot({
      width,
      marginTop: 40,
      marginBottom: 40,
      height: height,
      y: {
        label: "Variação (%)",
      },
      x: {
        tickFormat: d3.utcFormat("%b/%Y"),
        label: "Data",
        insetLeft: 36,
        tickSize: 0,
      },
      style: {
        fontSize: "12px",
      },
      marks: [
        Plot.axisY({
          tickSize: 0, // don’t draw ticks
          dx: 38, // offset right
          dy: -6, // offset up
          lineAnchor: "bottom", // draw labels above grid lines
          tickFormat: (d) => number_locale.format(".1%")(d)
        }),
        Plot.gridY({
          strokeDasharray: "5 5", // dashed
          strokeOpacity: 1, // opaque
          strokeWidth: 0.2  
        }),
        Plot.line(data_plot, {
          x: "data",
          y: d => d.valor / 100,
          stroke: "var(--theme-foreground-focus)",
          tip: {
            format: {
              x: d => d3.utcFormat("%b/%Y")(d),
              y: (d) => number_locale.format(".2%")(d),
            }
          },
          render: anim_line
        })
      ]
    });

    return plot;
}

function plot_comparacao_mes(width, serie) {
  const data_plot = aq.from(ipca_serie)
    .filter(aq.escape(d => d.variavel == serie))
    .filter(aq.escape(d => d.mes == mes_atual))
    .objects();

  const plot = Plot.plot({
      width,
      marginTop: 40,
      marginBottom: 40,
      height: 250,
      y: {
        label: "Variação (%)",
      },
      x: {
        label: "Ano",
        insetLeft: 36,
        tickSize: 0,
        interval: "year"
      },
      style: {
        fontSize: "12px",
      },
      marks: [
        Plot.axisY({
          tickSize: 0, // don’t draw ticks
          dx: 38, // offset right
          dy: -6, // offset up
          lineAnchor: "bottom", // draw labels above grid lines
          tickFormat: (d) => number_locale.format(".1%")(d)
        }),
        Plot.gridY({
          strokeDasharray: "5 5", // dashed
          strokeOpacity: 1, // opaque
          strokeWidth: 0.2
        }),
        Plot.barY(data_plot, 
          {
            x: "data",
            y: d => d.valor / 100,
            fill: "var(--theme-foreground-focus)",
            tip: {
              format: {
                x: d => d3.utcFormat("%Y")(d),
                y: (d) => number_locale.format(".2%")(d),
              }
            },
            render: anim_vbar    
        })
      ]
    })

    return plot;
}
```

<div class="grid grid-cols-2">
  <div class="card">
    <h2>Evolução do variação mensal</h2>
    ${resize((width) => plot_serie(width, series[0]))}
  </div>
  <div class="card">
    <h2>Evolução da variação acumulada em 12 meses</h2>
    ${resize((width) => plot_serie(width, series[2]))}
  </div>
  <div class="card">
    <h2> Comparações da variação mensal para o mesmo mês - ${mes_atual}</h2>
    ${resize((width) => plot_comparacao_mes(width, series[0]))}
  </div>
  <div class="card">
    <h2> Comparações da variação acumulada no ano para o mesmo mês - ${mes_atual}</h2>
    ${resize((width) => plot_comparacao_mes(width, series[1]))}
  </div>
</div>


```js
function plot_grupo(width, serie) {
  const data_plot = aq.from(ipca_grupo)
    .filter(aq.escape(d => d.variavel == serie))
    .filter(aq.escape(d => d.mes == mes_atual && d.ano == ano_atual))
    .filter(d => d.regiao == "Brasil")
    .objects()

  const plot = Plot.plot({
      width,
      height: 250,
      marginLeft: 150,
      y: {
        label: "Grupo",
        tickSize: 0
      },
      x: {
        label: "Variação (%)",
        tickSize: 0,
        tickFormat: number_locale.format(".2%"),
      },
      marks: [    
        Plot.gridX({
          strokeDasharray: "5 5", // dashed
          strokeOpacity: 1, // opaque
          strokeWidth: 0.2
        }),
        Plot.barX(
          data_plot,
          {
            y: "categoria",
            x: d => d.valor / 100,
            fill: "var(--theme-foreground-focus)",
            tip: {
              format: {
                y: d => d,
                x: (d) => number_locale.format(".2%")(d)
              }
            },
            render: anim_hbar       
          }
        )
      ]
    })

    return plot
}
```

<div class="grid grid-cols-3">
  <div class="card">
    <h2> Variação do IPCA por grupo - ${d3.utcFormat("%B/%Y")(data_max)}</h2>
    ${resize((width) => plot_grupo(width, series[0]))}
  </div>
  <div class="card">
    <h2> Variação do IPCA por grupo - Janeiro a ${d3.utcFormat("%B/%Y")(data_max)}</h2>
    ${resize((width) => plot_grupo(width, series[1]))}
  </div>
  <div class="card">
    <h2> Variação do IPCA por grupo - ${d3.utcFormat("%B/%Y")(data_min)} a ${d3.utcFormat("%B/%Y")(data_max)}</h2>
    ${resize((width) => plot_grupo(width, series[2]))}
  </div>  
</div>

```js
function plot_heatmap(width, serie) {
  const data_plot = aq.from(ipca_grupo)
    .filter(aq.escape(d => d.variavel == serie))
    .filter(d => d.regiao == "Brasil")
    .orderby(["data", "categoria"])
    .objects();

  const plot = Plot.plot({
        width,
        height: 250,
        marginLeft: 150,
        marginBottom: 40,
        x: {label: "Data", interval: "month", tickSize: 0},
        y: {label: "Grupo", tickSize: 0},
        color: {
          label: "Variação",
          legend: true,
          zero: true,
          scheme: "BrBg",
          tickFormat: number_locale.format(".2%"),
        },
        marks: [
          Plot.cell(
            data_plot,
            {
              x: "data",
              y: "categoria",
              fill: (d) => d.valor / 100,
              tip: {
                title: d => d.categoria,
                format: {
                  x: (d) => d3.utcFormat("%B/%Y")(d),
                  fill: (d) => number_locale.format(".2%")(d)
                }
              },
              render: anim_heatmap
            }
          )
        ]
      })

  return plot;
}
```

<div class="card">
  <h2>Variação do IPCA por grupo</h2>
  ${input_serie}
</div>
<div class="grid grid-cols-1">
  <div class="card grid-colspan-2">
    <h2>Evolução da variação do IPCA por grupo</h2>
    ${resize((width) => plot_heatmap(width, serie))}
  </div>
</div>

```js
const input_serie_sub = Inputs.select(
  series, {
    label: "Série",
    format: x => x.slice(7),
    value: series[0],
    width: 360
  });
const serie_sub = Generators.input(input_serie_sub);

function plot_histograma(width, serie) {
  const data_plot = aq.from(ipca_subitem)
    .filter(aq.escape(d => d.variavel == serie))
    .filter(d => d.regiao == "Brasil")
    .orderby(["data", "categoria"])
    .objects();

  const rect_mark = Plot.rectY(
    data_plot,
    Plot.binX(
      {y: "count"},
      {
        x: d => d.valor / 100,
        fill: "var(--theme-foreground-focus)",
        tip: {
          format: {
            x: d => number_locale.format(".2%")(d),          
            // replace "--" for " - -"
            y: d => d,
          }
        },
        render: anim_vbar
      }
    )
  );


  const plot = Plot.plot({
        width,
        height: 250,        
        marginBottom: 40,
        x: {label: "Variação (%)", tickSize: 0, insetLeft: 36, tickFormat: number_locale.format(".2%")},
        y: {label: "Frequência", tickSize: 0},
        marks: [
          Plot.gridY({
            strokeDasharray: "5 5", // dashed
            strokeOpacity: 1, // opaque
            strokeWidth: 0.2
          }),
          Plot.axisY({
            tickSize: 0, // don’t draw ticks
            dx: 38, // offset right
            dy: -6, // offset up
            lineAnchor: "bottom", // draw labels above grid lines
            tickFormat: (d) => number_locale.format(".0f")(d)
          }),
          rect_mark,
        ]
      })

    // const yScale = plot.scale("y");

    // const rects = d3.select(plot)
    //   .selectAll("[aria-label='rect']")
    //   .selectAll("rect");

    // const rects_data = rects.data();
    // rects._groups[0].forEach(
    //   function(d, i) {
    //     const height = d.attributes.height.value;
    //     const y = d.attributes.y.value;
    //     rects_data[i] = {
    //       "height": +height,
    //       "y": +y
    //     };
    //   }
    // );


    // // convert nodes in data
    // rects
    //   .data(rects_data)
    //   .attr("height", 0)
    //   .attr("y", d => yScale.apply(0))
    //   .transition()
    //   .duration(1000)
    //   // # use original height
    //   .attr("y", d => d.y)
    //   .attr("height", d => d.height);

    return plot;
}

function plot_var_subitem(width, serie, selecao, n) {

  let data_plot = aq.from(ipca_subitem)
    .filter(aq.escape(d => d.variavel == serie))
    .filter(d => d.regiao == "Brasil")
    .orderby("valor");
  
  if (selecao == "aumento") {
    data_plot = data_plot.slice(-n)
      .objects();
  } 

  if (selecao == "reducao") {
    data_plot = data_plot.slice(0, n)
      .objects();
  }

  const plot = Plot.plot({
    width,
    height: 250,
    marginBottom: 40,
    marginLeft: 120,
    y: {label: "Subitem", tickSize: 0},
    x: {label: "Variação (%)", tickSize: 0, tickFormat: number_locale.format(".2%")},
    marks: [
      Plot.axisY({
        tickSize: 0, // don’t draw ticks
        lineWidth: 10,
      }),
      Plot.gridX({
        strokeDasharray: "5 5", // dashed
        strokeOpacity: 1, // opaque
        strokeWidth: 0.2
      }),
      Plot.barX(
        data_plot,
        {
          y: "categoria",
          x: d => d.valor / 100,
          fill: selecao == "aumento" ? "var(--theme-foreground-focus)" : "#7e4a0b",
          tip: {
            format: {
              x: d => number_locale.format(".2%")(d),
              y: d => d
            }
          },
          sort: {y: "x", reverse: selecao == "aumento"},
          render: anim_hbar
        }
      )
    ]
  });

  return plot;

}

```

<div class="card">
  <h2>Variação do IPCA por subitem</h2>
  ${input_serie_sub}
</div>
<div class="grid grid-cols-3">
  <div class="card">
    <h2>Distruibuição da variação do IPCA por subitem</h2>    
    ${resize((width) => plot_histograma(width, serie_sub))}
  </div>
  <div class="card">
    <h2>Subitens com maiores aumentos</h2>
    ${resize((width) => plot_var_subitem(width, serie_sub, "aumento", 5))}
  </div>
  <div class="card">
    <h2>Subitens com maiores reduções</h2>
    ${resize((width) => plot_var_subitem(width, serie_sub, "reducao", 5))}
  </div>
</div>


```js
function anim_hbar(index, scales, values, dimensions, context, next) {
  const el = next(index, scales, values, dimensions, context);

  const rects = d3.select(el)
    .selectAll("rect");

  const rects_data = rects.data();
  rects._groups[0].forEach(
    function(d, i) {
      const x = d.attributes.x.value;
      const width = d.attributes.width.value;
      rects_data[i] = {
        "width": +width,
        "x": +x
      };
    }
  );
  
  const xScale = scales["x"];
  
  rects
    .data(rects_data)
    .attr("x", d => xScale(0.0))
    .attr("width", 0)
    .transition()
    .duration(1000)
    .attr("x", d => Math.min(xScale(0.0), d.x))
    .attr("width", d => d.width);

  return el;
}

function anim_vbar(index, scales, values, dimensions, context, next) {
  const el = next(index, scales, values, dimensions, context);

  const rects = d3.select(el)
    .selectAll("rect");

  const rects_data = rects.data();
  rects._groups[0].forEach(
    function(d, i) {
      const y = d.attributes.y.value;
      const height = d.attributes.height.value;
      rects_data[i] = {
        "height": +height,
        "y": +y
      };
    }
  );
  
  const yScale = scales["y"];
  
  rects
    .data(rects_data)
    .attr("y", d => yScale(0.0))
    .attr("height", 0)
    .transition()
    .duration(1000)
    .attr("y", d => Math.min(yScale(0.0), d.y))
    .attr("height", d => d.height);

  return el;
}

function anim_heatmap(index, scales, values, dimensions, context, next) {
  const el = next(index, scales, values, dimensions, context);

  const rects = d3.select(el)
    .selectAll("rect");

  rects
    .style("opacity", 0)
    .transition()
    .duration(100)
    .delay((d, i) => i * 1)
    .style("opacity", 1);

  return el;
}

function anim_line(index, scales, values, dimensions, context, next) {
  const el = next(index, scales, values, dimensions, context);

  const lines = d3.select(el)
    .selectAll("path");


  const height = context.ownerSVGElement.attributes.height.value;
  const width = context.ownerSVGElement.attributes.width.value;

  const defs = d3.select(el)
      .append('defs')
      .append('clipPath')
      .attr('id', 'clipEvol')
      .append('rect')
      .attr('height', height)
      .attr('width', 0);

  const xScale = scales["x"];

  lines
    .attr('clip-path', `url(#clipEvol)`);

  defs.transition()
    .duration(1000)
    .attr('width', width);

  return el;
}
```


<style>

:root {
  --theme-foreground-focus: #25798c;
  --theme-foreground-muted: #ffddc8;
  --theme-foreground-alt-heading: #242424;
}

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 1rem 0;
  padding: 1rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  color:#6f6f6f;
  /* background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor); */
  /* -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text; */
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

.card h1{
  color: var(--theme-foreground-alt-heading);
}

.card h2 {
  font-weight: bold;
  color: var(--theme-foreground-focus);
}

.card h3 {
  color: var(--theme-foreground-alt-heading);
}

.info {
  font-weight: 300;
  margin-bottom: 0;
  color: var(--theme-foreground-alt-heading);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
