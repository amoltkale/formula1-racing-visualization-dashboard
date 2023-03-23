function drawChart() {


    d3.selectAll("svg > *").remove()

    var tickDuration = 400;

    var top_n = 20;
    var height = 600;
    var width = 960;

    const margin = {
        top: 120,
        right: 0,
        bottom: 5,
        left: 0
    };

    let barPadding = (height - (margin.bottom + margin.top)) / (top_n * 5);

    let title = svg.append('text')
        .attr('class', 'title')
        .attr('y', 44)
        .html('FORMULA 1 RACING');

    let subTitle = svg.append("text")
        .attr("y", 75)
        .html("Bar Chart Race : Top 20 Drivers From 1950 to 2022");



    let year = 1950;
    let driver_name = 'Juan Fangio'


    d3.csv('drivers_over_years.csv').then(function (data) {
        //if (error) throw error;

        console.log(data);

        data.forEach(d => {
            d.value = +d.value,
                d.lastValue = +d.lastValue,
                d.value = isNaN(d.value) ? 0 : d.value,
                d.year = +d.year,
                d.colour = d3.hsl(Math.random() * 360, 0.75, 0.75)
        });

        console.log(data);

        let yearSlice = data.filter(d => d.year == year && !isNaN(d.value))
            .sort((a, b) => b.value - a.value)
            .slice(0, top_n);

        yearSlice.forEach((d, i) => d.rank = i);

        console.log('yearSlice: ', yearSlice)

        let x = d3.scaleLinear()
            .domain([0, d3.max(yearSlice, d => d.value)])
            .range([margin.left, width - margin.right - 65]);

        let y = d3.scaleLinear()
            .domain([top_n, 0])
            .range([height - margin.bottom, margin.top]);

        let xAxis = d3.axisTop()
            .scale(x)
            .ticks(width > 500 ? 5 : 2)
            .tickSize(-(height - margin.top - margin.bottom))
            .tickFormat(d => d3.format(',')(d));

        svg.append('g')
            .attr('class', 'axis xAxis')
            .attr('transform', `translate(0, ${margin.top})`)
            .call(xAxis)
            .selectAll('.tick line')
            .classed('origin', d => d == 0);

        svg.selectAll('rect.bar')
            .data(yearSlice, d => d.name)
            .enter()
            .append('rect')
            .attr('class', 'bar')
            .attr('x', x(0) + 1)
            .attr('width', d => x(d.value) - x(0) - 1)
            .attr('y', d => y(d.rank) + 5)
            .attr('height', y(1) - y(0) - barPadding)
            .style('fill', d => d.colour);

        svg.selectAll('text.label')
            .data(yearSlice, d => d.name)
            .enter()
            .append('text')
            .attr('class', 'label')
            .attr('x', d => x(d.value) - 8)
            .attr('y', d => y(d.rank) + 5 + ((y(1) - y(0)) / 2) + 1)
            .style('text-anchor', 'end')
            .html(d => d.name);

        svg.selectAll('text.valueLabel')
            .data(yearSlice, d => d.name)
            .enter()
            .append('text')
            .attr('class', 'valueLabel')
            .attr('x', d => x(d.value) + 5)
            .attr('y', d => y(d.rank) + 5 + ((y(1) - y(0)) / 2) + 1)
            .text(d => d3.format(',.0f')(d.value));

        let yearText = svg.append('text')
            .attr('class', 'yearText')
            .attr('x', width - margin.right)
            .attr('y', height - 20)
            .style('text-anchor', 'end')
            .html(~~year)
            .call(halo, 10);

        let caption = svg.append('text')
            .attr('class', 'caption')
            .attr('x', width - margin.right)
            .attr('y', height - 80)
            .style('text-anchor', 'end')
            .html(driver_name)
            .call(halo, 10);


        let ticker = d3.interval(e => {

            yearSlice = data.filter(d => d.year == year && !isNaN(d.value))
                .sort((a, b) => b.value - a.value)
                .slice(0, top_n);

            yearSlice.forEach((d, i) => d.rank = i);

            //console.log('IntervalYear: ', yearSlice);

            x.domain([0, d3.max(yearSlice, d => d.value)]);

            let max_val = d3.max(yearSlice, d => d.value);


            svg.select('.xAxis')
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .call(xAxis);

            let bars = svg.selectAll('.bar').data(yearSlice, d => d.name);

            bars
                .enter()
                .append('rect')
                .attr('class', d => `bar ${d.name.replace(/\s/g, '_')}`)
                .attr('x', x(0) + 1)
                .attr('width', d => x(d.value) - x(0) - 1)
                .attr('y', d => y(top_n + 1) + 5)
                .attr('height', y(1) - y(0) - barPadding)
                .style('fill', d => d.colour)
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('y', d => y(d.rank) + 5);

            bars
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('width', d => x(d.value) - x(0) - 1)
                .attr('y', d => y(d.rank) + 5);

            bars
                .exit()
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('width', d => x(d.value) - x(0) - 1)
                .attr('y', d => y(top_n + 1) + 5)
                .remove();

            let labels = svg.selectAll('.label')
                .data(yearSlice, d => d.name);

            labels
                .enter()
                .append('text')
                .attr('class', 'label')
                .attr('x', d => x(d.value) - 8)
                .attr('y', d => y(top_n + 1) + 5 + ((y(1) - y(0)) / 2))
                .style('text-anchor', 'end')
                .html(d => d.name)
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('y', d => y(d.rank) + 5 + ((y(1) - y(0)) / 2) + 1);


            labels
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value) - 8)
                .attr('y', d => y(d.rank) + 5 + ((y(1) - y(0)) / 2) + 1);

            labels
                .exit()
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value) - 8)
                .attr('y', d => y(top_n + 1) + 5)
                .remove();



            let valueLabels = svg.selectAll('.valueLabel').data(yearSlice, d => d.name);

            valueLabels
                .enter()
                .append('text')
                .attr('class', 'valueLabel')
                .attr('x', d => x(d.value) + 5)
                .attr('y', d => y(top_n + 1) + 5)
                .text(d => d3.format(',.0f')(d.value))
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('y', d => y(d.rank) + 5 + ((y(1) - y(0)) / 2) + 1);

            valueLabels
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value) + 5)
                .attr('y', d => y(d.rank) + 5 + ((y(1) - y(0)) / 2) + 1)
                .tween("text", function (d) {
                    let i = d3.interpolateRound(d.lastValue, d.value);
                    return function (t) {
                        this.textContent = d3.format(',')(i(t));
                    };
                });


            valueLabels
                .exit()
                .transition()
                .duration(tickDuration)
                .ease(d3.easeLinear)
                .attr('x', d => x(d.value) + 5)
                .attr('y', d => y(top_n + 1) + 5)
                .remove();

            yearText.html(~~year);
            caption.html(driver_name);

            if (year == 2022) ticker.stop();
            year = +year + 1;
            //console.log(year);
            const max_row = yearSlice.find(p => p.value == max_val);
            //console.log(max_row['name']);
            driver_name = max_row['name']
        }, tickDuration);

    });

    const halo = function (text, strokeWidth) {
        text.select(function () { return this.parentNode.insertBefore(this.cloneNode(true), this); })
            .style('fill', '#ffffff')
            .style('stroke', '#ffffff')
            .style('stroke-width', strokeWidth)
            .style('stroke-linejoin', 'round')
            .style('opacity', 1);

    }
}