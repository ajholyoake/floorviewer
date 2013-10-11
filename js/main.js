var $ = require('jquery')
//var d3 = require('d3')
//require('d3contour')
require('./jquery.csv-0.71.min.js');


$(function(){
//Set up events etc

$('.dropzone').each(function(){ 
$(this).on('dragover',function(){return false;});
$(this).on('dragend',function(){return false;});
$(this).on('drop',function(e){
getData(e,this)})});
});

function getData(e,item) {
//e is the event
//n is the side number

var $this = $(item);
var n = $this.attr('id').substr(1,1);

e.preventDefault();
var file = e.originalEvent.dataTransfer.files[0],
  reader = new FileReader();
  reader.onload = function(event){
  
  processData('#panel' + n,event.target.result,file);
  }
 // console.log(file);
  reader.readAsText(file);
}

//function drawData(el,data){
//
////Setup the drawing bits
//var margin = {top: 20, right: 20, bottom: 30, left: 30},
//    width = $(el).width() - margin.left - margin.right,
//    height = $(el).height() - margin.top - margin.bottom;
//
//var x = d3.scale.linear()
//    .range([0, width]);
//
//var y = d3.scale.linear()
//    .range([height, 0]);
//
//var color = d3.scale.linear()
//    .domain([95, 115, 135, 155, 175, 195])
//    .range(["#0a0", "#6c0", "#ee0", "#eb4", "#eb9", "#fff"]);
//
//var xAxis = d3.svg.axis()
//    .scale(x)
//    .orient("bottom")
//    .ticks(20);
//
//var yAxis = d3.svg.axis()
//    .scale(y)
//    .orient("left");
//
//var svg = d3.select(el).append("svg")
//    .attr("width", width + margin.left + margin.right)
//    .attr("height", height + margin.top + margin.bottom)
//  .append("g")
//    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
//
//
//d3.json("readme-heatmap.json", function(error, heatmap) {
//  var dx = heatmap[0].length,
//      dy = heatmap.length;
//
//  x.domain([0, dx]);
//  y.domain([0, dy]);
//
//  svg.selectAll(".isoline")
//      .data(color.domain().map(isoline))
//    .enter().append("path")
//      .datum(function(d) { return d3.geom.contour(d).map(transform); })
//      .attr("class", "isoline")
//      .attr("d", function(d) { return "M" + d.join("L") + "Z"; })
//      .style("fill", function(d, i) { return color.range()[i]; });
//
//  svg.append("g")
//      .attr("class", "x axis")
//      .attr("transform", "translate(0," + height + ")")
//      .call(xAxis);
//
//  svg.append("g")
//      .attr("class", "y axis")
//      .call(yAxis);
//
//  function isoline(min) {
//    return function(x, y) {
//      return x >= 0 && y >= 0 && x < dx && y < dy && heatmap[y][x] >= min;
//    };
//  }
//
//  function transform(point) {
//    return [point[0] * width / dx, point[1] * height / dy];
//  }
//});
//
//
//
//}


function getPicture(el,data){
  console.log(JSON.stringify(data));
  $.post("http://dev-performanceanalysis:5000/floorpng",JSON.stringify(data),function(retdata,textstatus,jqXHR)
  {
  $(el).find('img').remove();
   var imgholder = $(el).append($('<img src="data:image/png;base64,' + retdata + '" />'));
  //console.log(retdata);

  },'text');
}

function processTextFile(el,res,file){
  //remove trailing spaces
  res = res.replace(/[ ]*\n/g,'\n').replace(/[ ]+/g,',')
  var data = $.csv.toObjects(res);
  //Test with Cp

  getPicture(el,data);
  //drawData(el,data);
};

function processData(el,res,file){

var re = /(?:\.([^.]+))?$/;
var extension = re.exec(file.name)[1];

switch(extension)
{ 
  case 'txt':
  processTextFile(el,res,file);
  default:

}
  



}

//holder.ondrop = function (e) {
//  this.className = '';
//  e.preventDefault();
//
//  var file = e.dataTransfer.files[0],
//      reader = new FileReader();
//  reader.onload = function (event) {
//    console.log(event.target);
//    holder.style.background = 'url(' + event.target.result + ') no-repeat center';
//  };
//  console.log(file);
//  reader.readAsDataURL(file);
//
//  return false;
//};

