// d3 gallery https://d3-graph-gallery.com/graph/scatter_basic.html
// set the dimensions and margins of the graph
const margin = {top: 10, right: 30, bottom: 30, left: 60},
        width = 720 - margin.left - margin.right,
        height = 640 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

//Read the data
// csvParseRows: without header
// d3.text('data/xyz.csv').then(function(text) {
//     data = d3.csvParseRows(text);
//     scatterplot_visualize(data);
// })

// var test_data = JSON.parse('{{ feed_data | safe }}');
// console.log(test_data);


d3.csv('/data/test_office/data.csv').then(function(data) { // with header
    console.log(data);
    scatterplot_visualize(data);
})

function scatterplot_visualize(data) {
    // Add X axis
    const x = d3.scaleLinear()
    .domain([0, 1])
    .range([ 0, width ]);
    svg.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x));

    // Add Y axis
    const y = d3.scaleLinear()
    .domain([0, 1])
    .range([ height, 0]);
    svg.append("g")
    .call(d3.axisLeft(y));

    // Add dots
    svg.append('g')
    .selectAll("dot")
    .data(data)
    .join("circle")
        .attr("cx", function (d) { return x(d.centroid); } )
        .attr("cy", function (d) { return y(d.rms); } )
        .attr("r", 5)
        .style("fill", "#69b3a2")
        // .on("mouseover", highlight)
        // .on("mouseleave", doNotHighlight)
        .on("mouseover", function(event, d) {
            d3.select(this)
              .transition()
              .duration(100)
              .attr("r", 10);
        })
        .on("mouseleave", function(event, d) {
            d3.select(this)
              .transition()
              .duration(100)
              .attr("r", 5);
        })
}