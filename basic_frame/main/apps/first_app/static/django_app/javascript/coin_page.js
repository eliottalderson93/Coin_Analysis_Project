var data = [30,86,168,281,303,265];

d3.select(".chart")
	.selectAll("div")
	.data(data)
		.enter()
		.append("div")
		.style("width", function(d) {return d})
		.text(function(d){ return + d});