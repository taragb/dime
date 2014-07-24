var jsdom = require('jsdom');
var CloudConvert = require('/Users/tyson/node_modules/cloud-convert/dist/cloud-convert.min.js').CloudConvert;


jsdom.env(
  "<html><body></body></html>",
  [ 'http://d3js.org/d3.v3.min.js'],
  function (err, window) {

    var config  = __dirname + '/config.yml',
    file    = __dirname + '/test.svg';

    var $task  = new CloudConvert(config).convert(file).from('svg').into('pdf').process();

    $task.when('finished', function(data) {
      console.log("Let's download " + data.output.url);
    });


    var svg = window.d3.select("body")
        .append("svg")
        .attr("width", 100).attr("height", 100);

    svg.append("rect")
        .attr("x", 10)
        .attr("y", 10)
        .attr("width", 80)
        .attr("height", 80)
        .style("fill", "orange");

    svg.append("text")
      .attr("x", 10)
      .attr("y", 50)
      .attr("font-family", "Gotham-ExtraLight")
      .text("The quick brown dog");


    console.log(window.d3.select("body").html());
  }
);