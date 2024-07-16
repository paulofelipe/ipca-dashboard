import * as d3 from "../../_npm/d3@7.9.0/_esm.js";

export const locale = d3.timeFormatDefaultLocale({
  dateTime: "%A, %e de %B de %Y. %X",
  date: "%d/%m/%Y",
  time: "%H:%M:%S",
  periods: ["AM", "PM"],
  days: ["Domingo", "Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"],
  shortDays: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
  months: ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"],
  shortMonths: ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]
});

export const number_locale = d3.formatLocale({
  decimal: ",",
  thousands: ".",
  grouping: [3],
  currency: ["R$", ""]
});