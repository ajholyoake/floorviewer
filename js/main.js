var $ = require('jquery')
//var d3 = require('d3')
//require('d3contour')
require('./jquery.csv-0.71.min.js');



var sign = [null,null];
var d = [[],[]];
$(function(){
//Set up events etc
//

$('.dropzone').each(function(){ 
$(this).on('dragover',function(){return false;});
$(this).on('dragend',function(){return false;});
$(this).on('drop',function(e){
getData(e,this)})});

$('.field-select').on('change',function(e){plotGraphs(this);});

});

function getData(e,item) {
var $this = $(item);
var n = parseFloat($this.attr('id').substr(1,1));

e.preventDefault();
var file = e.originalEvent.dataTransfer.files[0],
  reader = new FileReader();
  reader.onload = function(event){
  processFile(n,event.target.result,file);
  }
  reader.readAsText(file);
}

function processFile(n,res,file){
  
  var el = $('#panel' + n);
  $('#filename' + n).text(file.name);
  var re = /(?:\.([^.]+))?$/;
  var extension = re.exec(file.name)[1];

  //res = res.replace(/[ ]*\n/g,'\n').replace(/[ ]+/g,',')
  switch(extension){
  case 'txt':
    res = res.replace(/[ ]*\n/g,'\n').replace(/[ ]+/g,',')
    }
  
    res = res.replace(/ /g,'');


  var td = $.csv.toObjects(res);
  td.forEach(function(el){ 
    if (el.x)
    {
    el.X = el.x; 
    delete(el.x)
    }
    if (el.y)
    {
    el.Y = el.y;
    delete(el.y);
    }
    }
  );

  var signs = null;

  var signs = td.map(function(el){
    if (el.Y > 0) return 1;
    else if (el.Y < 0) return -1;
    else return 0});
  
  var samesign = true;
  signs.forEach(function(el){ samesign = samesign && el == signs[0]});
  sign[n-1] = samesign ? signs[0] : 0; 



  //td.forEach(function(el){
  //if (el.Y > 0){
  //reflect = (reflect && (signs === 1 || signs == null));
  //signs = 1;
  //} else if(el.Y < 0) {
  //  reflect = (reflect && (signs === -1 || signs == null));
  //  signs = -1;
  //};
  //});


  //if(reflect){
  //  var td2 = $.csv.toObjects(res); //ugh
  //  td2.forEach(function(el){
  //    var tel = $.extend({},el);
  //    tel.Y = -tel.Y;
  //    td.push(tel);
  //  });
  //}

  d[n-1] = td;


  $('#select' + n + '>option').remove();
  //Add entries into the selects, put in appropriate data structure and send both over. Consider caching responses
  for(var k in d[n-1][0]){
  if(k.length > 0 & k !== 'X' & k !== 'Y')
  {
  $('#select' + n).append($('<option>',{value:k}).text(k));
  }
  }
  $('#select' + n).css({opacity: 1});
  
  //Now process the data appropriately
  plotGraphs();
}

function reflect(td){
var td2 = $.extend([],td);
td2.forEach(function(el){
var tel = $.extend({},el);
tel.Y = (-parseFloat(el.Y)) + ''; 
td.push(tel)}
);
}

function plotGraphs(el)
{
  var a = [[],[]];
  var fields = [$('#select1').val(), $('#select2').val()];
  d[0].length && d[0].forEach(function(obj){a[0].push({X:obj.X,Y:obj.Y, Z:obj[fields[0]]})});
  d[1].length && d[1].forEach(function(obj){a[1].push({X:obj.X,Y:obj.Y, Z:obj[fields[1]]})});
  
  if (sign[0] != null && sign[0] === 0 && (sign[1] === -1 || sign[1] == 1)) reflect(a[1]);
  if (sign[1] != null && sign[1] === 0 && (sign[0] === -1 || sign[0] == 1)) reflect(a[0]);
  if (sign[1] !== 0 && (sign[1] === -1*sign[0])){ reflect(a[1]); reflect(a[0]); };
  


  $(el).closest('.bigpanel').find('img').remove();
  $('#deltarow').find('img').remove();

  var connect_string =  "http://dev-performanceanalysis/floorviewer/generate";
  //connect_string = "http://dev-performanceanalysis:5000/floorviewer/generate";
  $.post(connect_string,JSON.stringify(a),function(retdata,textstatus,jqXHR)
  {
  var pngs = JSON.parse(retdata);
  for (var ii =0; ii < pngs.length; ii++)
  {
  $('#panel' + (ii+1)).find('img').remove();
  if(pngs[ii].length > 0)
  {
  $('#panel' + (ii+1)).append($('<img src="data:image/png;base64,' + pngs[ii] + '" />'));
  }
  if(ii === 2){
  $('#deltarow').css({opacity:1});
  }
  }
  },'text');


}

