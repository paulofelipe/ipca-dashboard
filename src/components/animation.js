import * as d3 from "npm:d3";

export function anim_hbar(index, scales, values, dimensions, context, next) {
  const el = next(index, scales, values, dimensions, context);

  const rects = d3.select(el)
    .selectAll("rect");

  const rects_data = rects.data();
  rects._groups[0].forEach(
    function (d, i) {
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
    .attr("x", xScale(0.0))
    .attr("width", 0)
    .transition()
    .duration(1000)
    .attr("x", d => Math.min(xScale(0.0), d.x))
    .attr("width", d => d.width);

  return el;
}

export function anim_vbar(index, scales, values, dimensions, context, next) {
  const el = next(index, scales, values, dimensions, context);

  const rects = d3.select(el)
    .selectAll("rect");

  const rects_data = rects.data();
  rects._groups[0].forEach(
    function (d, i) {
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
    .attr("y", yScale(0.0))
    .attr("height", 0)
    .transition()
    .duration(1000)
    .attr("y", d => Math.min(yScale(0.0), d.y))
    .attr("height", d => d.height);

  return el;
}

export function anim_heatmap(index, scales, values, dimensions, context, next) {
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

export function anim_line(index, scales, values, dimensions, context, next) {
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


  lines
    .attr('clip-path', `url(#clipEvol)`);

  defs.transition()
    .duration(1000)
    .attr('width', width);

  return el;
}