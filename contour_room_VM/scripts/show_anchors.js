var width = 0;
var height = 0;
var start = 0;
var end = 0;
var step = 0;
var xs =[]
var ys = []
var canvasx = 300;
var canvasy = 150;
var sample_distance = 0;

function validInput(){
    var input = document.getElementById("line").value;
    var curWidth = parseInt(document.getElementById("contour").style.width);
    if(userinput){

        // define(['require'], function (require) {
        //     define(['child_process'],function(child_process){
        //         require(["child_process"], function (cp) {
        //             var spawn = cp.spawn;
        //             console.log('here');
        //             var variable = spawn("python3",["contour_server.py"]);
        //             console.log("get here");
        //             spawn("python3",["generic_server.py"]);
        //             // require('child_process').exec('python3 ../contour_server.py');
        //         });
        //     });
        // });
        
        // console.log('out here');
        // require(["child_process"], function (cp) {
        //     var spawn = cp.spawn;
        //     spawn("python3",["../contour_server.py"]);
        //     // spawn("python3",["../generic_server.py"]);
        //     // require('child_process').exec('python3 ../contour_server.py');
        // });

        // const { spawn } = require(["child_process"]);

        // // alias spawn
        // const exec = (commands) => {
        //   spawn(commands, { stdio: "inherit", shell: true });
        // };
        
        // // use like this
        // exec("python3 ../contour_server.py");

        // spawn("python3",["../contour_server.py"]);
        // require('child_process').exec('python3 ../contour_server.py');
        
        // const {spawn} = require("child_process");
        // spawn("python3",["contour_server.py"]);
        // spawn("python3",["generic_server.py"]);
        const inputs = input.split("=");
        const coors = inputs[2].substring(0,inputs[2].length-9).split("*");
        // console.log(coors);
        width = parseInt(coors[0]);
        height = parseInt(coors[1]);
        var scale = height/width;
        const gradient = inputs[3].split(';');
        start = gradient[0];
        end = gradient[1];
        step = gradient[2].substring(0,gradient[2].length-15);
        sample_distance = parseInt(inputs[4]);
        // console.log(inputs[1])
        const anchors = inputs[1].substring(0,inputs[1].length-9).split(";");
        const canvas = document.getElementById("canvas");
        var ctx = document.getElementById("canvas").getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        // console.log(anchors);
        for(var i =0; i<anchors.length;i++){
            const locs = anchors[i].split(",");
            // console.log(locs);
            // console.log(parseInt(locs[0])*300/width);
            xs.push(parseInt(locs[0])*canvasx/width);
            ys.push(canvasy-parseInt(locs[1])*canvasy/height);
        }
        // console.log(xs);
        // console.log(ys);
        document.getElementById("contour").style.height = (scale*curWidth).toString()+"px";
        var pointSize = 3;

    //     draw.onClick(function(e){
    //         getPosition(e); 
    //    });

        function getPosition(x,y){
            // var rect = canvas.getBoundingClientRect();
            // var x = x+rect.left;
            // var y = y+rect.top;
            var x = x;
            var y = y;
            // var x = event.clientX-rect.left;
            // var y = event.clientY-rect.top;
            // console.log("x");
            // console.log(x);
            // console.log('y');
            // console.log(y);
            drawCoordinates(x,y);
       }

        function drawCoordinates(x,y){	
            // var ctx = document.getElementById("canvas").getContext("2d");
      
            ctx.fillStyle = "black"; // Red color
      
          ctx.beginPath();
          ctx.arc(x, y, pointSize, 0, Math.PI * 2);
          ctx.fill();
          ctx.stroke();
        // ctx.fillStyle = "#FF0000";
        // ctx.fillRect(0, 0, 150, 75);
        //   console.log(ctx)
        //   console.log('should draw')
      }

    //   for (var i = 0; i< xs.length; i++){
    //     getPosition(xs[i],ys[i]);
    //   }
    

        function createCORSRequest(method, url){
            var xhr = new XMLHttpRequest();
            if ("withCredentials" in xhr){
                xhr.open(method, url, true);
            } else if (typeof XDomainRequest != "undefined"){
                xhr = new XDomainRequest();
                xhr.open(method, url);
            } else {
                xhr = null;
            }
            return xhr;
        }

        const url = "http://localhost:8081/path?"+input;
        var http = createCORSRequest("get", url);
        // console.log(url)
        contour_map = document.getElementById('contour');
        map = document.getElementById('map');

        http.onload = function ()
        {
            if (this.status >= 200 && this.status < 400)
            {
                // Success!
                // console.log("get here")
                // console.log(this.response)
                var data = JSON.parse(this.response);
                var x_axis = [];
                for (var i = 0; i <= width;i = i+sample_distance) {
                    // console.log(i);
                    x_axis.push(i);
                }
                var y_axis = [];
                for (var i = 0; i <= height;i = i+sample_distance) {
                    y_axis.push(i);
                }
                console.log('x_axis:');
                console.log(x_axis);
                console.log("y_axis:");
                console.log(y_axis);
                console.log("data y size:");
                console.log(data.length);
                console.log("data x size: ");
                console.log(data[0].length);
                var contour_data = [{
                    z: data,
                    type: 'contour',
                    // colorscale:"Jet",
                    x: x_axis,
                    y: y_axis,
                    contours : {
                        start :start,
                        end :end,
                        size :step},
                    contours: {
                        coloring: 'heatmap',
                        showlabels: true,
                        labelfont: {
                            family: 'Raleway',
                            size: 12,
                            color: 'white',
                        }
                        }
                }];

                // var layout = {
                //     title: 'Colorscale for Contour Plot'
                //   };
                  var layout = {
                    autosize: false,
                    width: 500,
                    height: 500,
                    title: 'Colorscale for Contour Plot',
                    automargin: false,

                    xaxis:{range: [0,width]},
                    yaxis:{range: [0,height]}
                    // xaxis: {
                    //     autotick: false,
                    //     ticks: 'outside',
                    //     tick0: 0,
                    //     dtick: 200,
                    //     ticklen: width,
                    //     tickwidth: 4,
                    //     tickcolor: '#000'
                    //   },
                    //   yaxis: {
                    //     autotick: false,
                    //     ticks: 'outside',
                    //     tick0: 0,
                    //     dtick: 200,
                    //     ticklen: height,
                    //     tickwidth: 4,
                    //     tickcolor: '#000'
                    //   }
                    // margin: {
                    //   l: 50,
                    //   r: 50,
                    //   b: 100,
                    //   t: 100,
                    //   pad: 4
                    // },
                }
                Plotly.newPlot(contour_map, contour_data, layout);
                console.log(data);
                
                for (var i = 0; i< xs.length; i++){
                    console.log('reach here')
                    getPosition(xs[i],ys[i]);
                }
                xs = [];
                ys = [];
            } else
            {
                // We reached our target server, but it returned an error.
                console.log("Error status not between 200 and 400.");
            }
        };

        http.onerror = function (e)
        {
            // There was a connection error of some sort.
            console.log(e);
        };

        http.send();
    }
    
}