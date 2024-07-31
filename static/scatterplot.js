// data_csv = d3.csv("/data/xyz.csv", function(data) {
// var data = feed_data;
var width = 928;
var height = 600;
var k = height/width;

const zoom = d3.zoom()
    .scaleExtent([0.5, 32])
    .on("zoom", zoomed);

const svg = d3.create("svg")
    .attr("viewBox", [0, 0, width, height]);

const gGrid = svg.append("g");

const gDot = svg.append("g")
    .attr("fill", "none")
    .attr("stroke-linecap", "round");

// var data = {
//     random = d3.randomNormal(0, 0.2);
//     sqrt3 = Math.sqrt(3);
//     return [].concat(
//         Array.from({length: 20}, () => [random() + sqrt3, random() + 1, 0]),
//         Array.from({length: 20}, () => [random() - sqrt3, random() + 1, 1]),
//         Array.from({length: 20}, () => [random(), random() - 1, 2])
//     );
// }

const numPoints = 32;
const data = [];
for (let i = 0; i < numPoints; i++) {
  data.push([Math.random() * (1.5 - -1.5) + -1.5, Math.random() * (1.5 - -1.5) + -1.5, 0]); // x y z
}

gDot.selectAll("path")
    .data(data) // 
    .join("path")
    .attr("d", d => `M${x(d[0])},${y(d[1])}h0`)
    .attr("stroke", d => z(d[2]));

const gx = svg.append("g");

const gy = svg.append("g");

svg.call(zoom).call(zoom.transform, d3.zoomIdentity);

var x = d3.scaleLinear()
    .domain([-1.5, 1.5])
    .range([0, width])

var y = d3.scaleLinear()
    .domain([-1.5 * k, 1.5 * k])
    .range([height, 0])

var z = d3.scaleOrdinal()
    .domain(data.map(d => d[2]))
    .range(d3.schemeCategory10)

xAxis = (g, x) => g
    .attr("transform", `translate(0,${height})`)
    .call(d3.axisTop(x).ticks(12))
    .call(g => g.select(".domain").attr("display", "none"))

yAxis = (g, y) => g
    .call(d3.axisRight(y).ticks(12 * k))
    .call(g => g.select(".domain").attr("display", "none"))

grid = (g, x, y) => g
    .attr("stroke", "currentColor")
    .attr("stroke-opacity", 0.1)
    .call(g => g
      .selectAll(".x")
      .data(x.ticks(12))
      .join(
        enter => enter.append("line").attr("class", "x").attr("y2", height),
        update => update,
        exit => exit.remove()
      )
        .attr("x1", d => 0.5 + x(d))
        .attr("x2", d => 0.5 + x(d)))
    .call(g => g
      .selectAll(".y")
      .data(y.ticks(12 * k))
      .join(
        enter => enter.append("line").attr("class", "y").attr("x2", width),
        update => update,
        exit => exit.remove()
      )
        .attr("y1", d => 0.5 + y(d))
        .attr("y2", d => 0.5 + y(d)));

function zoomed({transform}) {
    const zx = transform.rescaleX(x).interpolate(d3.interpolateRound);
    const zy = transform.rescaleY(y).interpolate(d3.interpolateRound);
    gDot.attr("transform", transform).attr("stroke-width", 5 / transform.k);
    gx.call(xAxis, zx);
    gy.call(yAxis, zy);
    gGrid.call(grid, zx, zy);
}

// return Object.assign(svg.node(), {
//     reset() {
//     svg.transition()
//         .duration(750)
//         .call(zoom.transform, d3.zoomIdentity);
//     }
// });

