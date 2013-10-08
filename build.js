"use strict";

var request = require('request')
  , fs      = require('fs')
  , path = require('path')
  , browserify = require('browserify')
  , shim = require('browserify-shim')
  , watchify = require('watchify')
  , through  = require('through')
  , exec = require('child_process').exec
  ;

function bundleOuter(){
  // This is function is the important part and should be similar to what you would use for your project
  var builtFile = path.join(__dirname, 'js/build/bundle.js');
  var dotFile   = path.join(path.dirname(builtFile), '.' + path.basename(builtFile));
  var w;
  shim( w = watchify(), {
      jquery:   { path: './js/vendor/jquery-1.10.1.min.js', exports: '$' },
      d3:       { path: './js/vendor/d3.v3.min.js',     exports: 'd3'},
      d3contour:{ path: './js/contour.js', exports:null},
      bootstrap:{ path: './js/vendor/bootstrap.min.js', exports:null},
      modernizr:{ path: './js/vendor/modernizr-2.6.2-respond-1.1.0.min.js', exports:null}
  })
  .require(require.resolve('./js/main.js'), { entry: true });
  

  w.on('update',function(){bundle(); });
  bundle();

function bundle() {
    var wb = w.bundle(); //Source maps on - doesn't work. (supply {debug:true})
    wb.on('error',function(err){
    console.error(String(err));
    exec('notifu64 /p "Timing build error" /m "' + String(err) + '" /d 3' );
    });

    wb.pipe(fs.createWriteStream(dotFile));
    var bytes = 0;
    wb.pipe(through(write,end));

    function write(buf) {bytes += buf.length}

    function end(){
    exec('notifu64 /p "Timing built" /m "' + bytes + ' bytes written to ' + builtFile + '" /d 3' ); //@notifu /p "Hello, World!" /m "Thank you for giving my Notifu utility a try. I hope it will make you a hero (or at least make your life easier).\n\n(this notification will disapear after 15 seconds)" /d 15 /i notifu.exe
     fs.rename(dotFile,builtFile, function(err){
     var outstring = bytes + ' bytes written to ' + builtFile;

     if(err){
     outstring = String(err); 
     exec('notifu64 /p "Timing build error" /m "' + outstring + '" /d 3' );
     console.log(outstring);
     }
     console.error(outstring);
     exec('notifu64 /p "Timing built" /m "' + outstring + '" /d 3' );

  });
}
}
}


// Normally jquery.js would be in vendor folder already, but I wanted to avoid spreading jquerys all over github ;)
//request('http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', function(err, resp, body) {
//  var jqueryFile = path.join(__dirname, 'js/vendor/jquery.js');

//  fs.writeFileSync(jqueryFile, body);

//request('http://d3js.org/d3.v3.min.js', function(err, resp, body) {
//  var d3File = path.join(__dirname, 'js/vendor/d3.js');

//  fs.writeFileSync(d3File, body);

 bundleOuter();
//});
//});
