console.log("its working")

function parseData(data){
	var dataResponse = [];
	for (i = 0; i < data.length; i++ )
	{
		dataResponse.push(
		{
			date: new Date(data[i]['time']),
			value: +data[i]['price']
		});
	}
	return dataResponse
}


function drawChart(data,theDiv) {
	var svgWidth = 800, svgHeight = 500;
	var margin = { top: 20, right: 20, bottom: 30, left: 50 };
	var width = svgWidth - margin.left - margin.right;
	var height = svgHeight - margin.top - margin.bottom;

	var svg = d3.select(".line-chart")
	.attr("width", svgWidth)
	.attr("height", svgHeight);

	var g = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var x = d3.scaleTime()
	.rangeRound([0, width]);

	var y = d3.scaleLinear()
	.rangeRound([height, 0]);

	var line = d3.line()
	.x(function(d) { return x(d.date)})
	.y(function(d) { return y(d.value)})
	x.domain(d3.extent(data, function(d) { return d.date }));
	y.domain(d3.extent(data, function(d) { return d.value }));

	g.append("g")
	.attr("transform", "translate(0," + height + ")")
	.call(d3.axisBottom(x))
	.select(".domain")
	.remove();

	g.append("g")
	.call(d3.axisLeft(y))
	.append("text")
	.attr("fill", "#000")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", "0.71em")
	.attr("text-anchor", "end")
	.text("Price ($)");

	g.append("path")
	.datum(data)
	.attr("fill", "none")
	.attr("stroke", "steelblue")
	.attr("stroke-linejoin", "round")
	.attr("stroke-linecap", "round")
	.attr("stroke-width", 1.5)
	.attr("d", line);
}
function drawChart2(data, theDiv) {
	var svgWidth = 800, svgHeight = 500;
	var margin = { top: 20, right: 20, bottom: 30, left: 50 };
	var width = svgWidth - margin.left - margin.right;
	var height = svgHeight - margin.top - margin.bottom;

	var svg = d3.select(theDiv)
	.attr("width", svgWidth)
	.attr("height", svgHeight);

	var g = svg.append("g")
	.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var x = d3.scaleTime()
	.rangeRound([0, width]);

	var y = d3.scaleLinear()
	.rangeRound([height, 0]);

	var line = d3.line()
	.x(function(d) { return x(d.date)})
	.y(function(d) { return y(d.value)})
	x.domain(d3.extent(data, function(d) { return d.date }));
	y.domain(d3.extent(data, function(d) { return d.value }));

	g.append("g")
	.attr("transform", "translate(0," + height + ")")
	.call(d3.axisBottom(x))
	.select(".domain")
	.remove();

	g.append("g")
	.call(d3.axisLeft(y))
	.append("text")
	.attr("fill", "#000")
	.attr("transform", "rotate(-90)")
	.attr("y", 6)
	.attr("dy", "0.71em")
	.attr("text-anchor", "end")
	.text("Price ($)");

	g.append("path")
	.datum(data)
	.attr("fill", "none")
	.attr("stroke", "steelblue")
	.attr("stroke-linejoin", "round")
	.attr("stroke-linecap", "round")
	.attr("stroke-width", 1.5)
	.attr("d", line);
}

// Alan Duling sample modified to work for this project
function interactiveChart(id, theDiv){

	if (id === 1){
		URL = "http://localhost:8000/jss";
	}
	else if (id === 825){
		URL = "http://localhost:8000/jss2";
	}
	else{
		URL = "http://localhost:8000/jss";
	}

	var svg = d3.select(theDiv),
    margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = +svg.attr("width") - margin.left - margin.right,
    height = +svg.attr("height") - margin.top - margin.bottom;

var parseTime = d3.timeParse("%d")
    bisectDate = d3.bisector(function(d) { return d.year; }).left;

var x = d3.scaleTime().rangeRound([0, width]);
var y = d3.scaleLinear().rangeRound([height, 0]);

var line = d3.line()
    .x(function(d) { return x(d.year); })
    .y(function(d) { return y(d.value); });

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

d3.json(URL, function(error, data) {
    if (error) throw error;

    data.forEach(function(d) {
      d.time = parseTime(d.time);
      d.value = +d.value;
    });

    x.domain(d3.extent(data, function(d) { return d.year; }));
    y.domain(d3.extent(data, function(d) { return d.value; }));

    g.append("g")
        .attr("class", "axis axis--x")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(15).tickFormat(function(d) { return parseInt(d * 1); }))

    g.append("g")
        .attr("class", "axis axis--y")
        .call(d3.axisLeft(y).ticks(3).tickFormat(function(d) { return parseInt(d / 1000) + "k"; }))
      .append("text")
        .attr("class", "axis-title")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .attr("fill", "#5D6971")
        .text("Price");

    g.append("path")
        .datum(data)
        .attr("class", "line")
        .attr("d", line);

    var focus = g.append("g")
        .attr("class", "focus")
        .style("display", "none");

    focus.append("line")
        .attr("class", "x-hover-line hover-line")
        .attr("y1", 0)
        .attr("y2", height);

    focus.append("line")
        .attr("class", "y-hover-line hover-line")
        .attr("x1", width)
        .attr("x2", width);

    focus.append("circle")
        .attr("r", 7.5);

    focus.append("text")
        .attr("x", 15)
        .attr("dy", ".31em");

    svg.append("rect")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
        .attr("class", "overlay")
        .attr("width", width)
        .attr("height", height)
        .on("mouseover", function() { focus.style("display", null); })
        .on("mouseout", function() { focus.style("display", "none"); })
        .on("mousemove", mousemove);

    function mousemove() {
      var x0 = x.invert(d3.mouse(this)[0]),
          i = bisectDate(data, x0, 1),
          d0 = data[i - 1],
          d1 = data[i],
          d = x0 - d0.year > d1.year - x0 ? d1 : d0;
      focus.attr("transform", "translate(" + x(d.year) + "," + y(d.value) + ")");
      focus.select("text").text(function() { return d.value; });
      focus.select(".x-hover-line").attr("y2", height - y(d.value));
      focus.select(".y-hover-line").attr("x2", width + width);
    }
});

}