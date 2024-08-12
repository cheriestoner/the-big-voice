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

// d3.csv('/data/{{audiofile}}/data.csv').then()


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

    // Create an audio element
    const audioElement = document.createElement('audio');
    audioElement.src = '/audio/test_office.wav'; // 加载完整的音频文件
    document.body.appendChild(audioElement);

    let isUserInteracted = false;
    // Listen for user interaction
    document.body.addEventListener('pointerdown', function () {
        isUserInteracted = true;
    });

    // Add dots
    svg.append('g')
    .selectAll("dot")
    .data(data)
    .join("circle")
        .attr("cx", function (d) { return x(d.centroid); } )
        .attr("cy", function (d) { return y(d.rms); } )
        .attr("r", 7.5)
        .style("fill", "#24d00a")
        
        .on("mouseover", function(event, d) {
            d3.select(this)
              .transition()
              .duration(200)
              .attr("r", 15);
            
            if (isUserInteracted) {
                const startTime = parseFloat(d.start_time_sec);
                const endTime = parseFloat(d.end_time_sec);
                if (!isNaN(startTime) && !isNaN(endTime) && startTime < endTime) {
                    // Set audio to start time and play
                    audioElement.currentTime = startTime;
                    audioElement.play();
                    // Calculate duration
                    const duration = endTime - startTime;
                    // Stop audio
                    setTimeout(() => {
                        audioElement.pause();
                        audioElement.currentTime = 0; // Reset to start
                    }, duration * 1000); // Convert duration to milliseconds
                } else {
                    console.error("Invalid start or end time:", d.start_time_sec, d.end_time_sec);
                }
            }
        })
        .on("mouseleave", function(event, d) {
            d3.select(this)
              .transition()
              .duration(200)
              .attr("r", 7.5);
            //停止播放
            audioElement.pause();
            audioElement.currentTime = 0; //重置
        })
}