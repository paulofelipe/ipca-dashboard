---
toc: false
theme: [wide, air, alt]
---

```js
import {locale, number_locale} from "./components/locale.js";
```

<h1>IPCA</h1>
<h2>Dashboard com informações detalhadas do Índice de Preços ao Consumidor Amplo (IPCA)</h2>
<p>Os dados utilizados neste dashboard são originários do sistema SIDRA do IBGE e estão disponíveis para download <a href="https://sidra.ibge.gov.br/pesquisa/snipc/ipca/tabelas">aqui</a>.</p>


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
