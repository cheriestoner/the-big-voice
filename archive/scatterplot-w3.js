// https://www.w3schools.com/ai/ai_d3js.asp
// Set Dimensions
const xSize = 500; 
const ySize = 500;
const margin = 40;
const xMax = xSize - margin*2;
const yMax = ySize - margin*2;

data = []
d3.text('data/xyz.csv').then(function(text) {
    data = d3.csvParseRows(text);
    console.log(data);
    visualizeCSV(data);
});

function visualizeCSV(data) {

    // Append SVG Object to the Page
    const svg = d3.select("#myPlot")
    .append("svg")
    .append("g")
    .attr("transform","translate(" + margin + "," + margin + ")");

    // X Axis
    const x = d3.scaleLinear()
    .domain([0, 1]) // input domainxt
    .range([0, xMax]); //output range

    svg.append("g")
    .attr("transform", "translate(0," + yMax + ")")
    .call(d3.axisBottom(x));

    // Y Axis
    const y = d3.scaleLinear()
    .domain([0, 1])
    .range([ yMax, 0]);

    svg.append("g")
    .call(d3.axisLeft(y));

    // Dots
    svg.append('g')
    .selectAll("dot")
    .data(data).enter()
    .append("circle")
    .attr("cx", function (d) { return x(d[0]) } )
    .attr("cy", function (d) { return y(d[1]) } )
    .attr("r", 3)
    .style("fill", "#69b3a2");
}