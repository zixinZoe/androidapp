// const { Dictionary } = require("requirejs");

var width = 0;
var height = 0;
// var start = 0;
// var end = 0;
// var step = 0;
var xs =[];
var ys = [];
var canvasx = 300;
var canvasy = 150;
var sample_distance = 0;

var input = "";
var anchorLoc = "";
var roomSize = "";
// var gradient = "";
var sampleDistance = "";
var sigma = "";
var maxErrShown = "";
var iniSeed = "";
var customSeed = "";
var dop = "";

function overss(){
// ss = document.getElementById("ss");
// ss.addEventListener("mouseover", function( event ) {
    ss.style.color = "red";
    anchorLoc = "150,150;150,250;250,150;250,250";
    roomSize = "400*400";
    // gradient = "0;3000;100";
    sampleDistance = "200";
    sigma = "50";
    maxErrShown = "50";
    iniSeed = "roomCenter";
    customSeed = "20,20";
    dop = "all";
    count = "50";

    document.getElementById("anchorloc").value = anchorLoc;
    document.getElementById("roomsize").value = roomSize;
    document.getElementById("sigma").value = sigma;
    // gradient = document.getElementById("gradient").value;
    document.getElementById("sampledistance").value = sampleDistance;
    document.getElementById("maxerrshown").value = maxErrShown;
    document.getElementById("iniseed").value = iniSeed;
    document.getElementById("customseed").value = customSeed;
    document.getElementById("dop").value = dop;
    document.getElementById("count").value = count;
// });
}

function change(){
    // ss = document.getElementById("ss");
    // ss.addEventListener("mouseover", function( event ) {
        input = document.getElementById("ex_inputs");
        if(input.value == "ss"){
            anchorLoc = "150,150;150,250;250,150;250,250";
            roomSize = "400*400";
            // gradient = "0;3000;100";
            sampleDistance = "200";
            sigma = "50";
            maxErrShown = "50";
            iniSeed = "roomCenter";
            customSeed = "20,20";
            dop = "all";
            count = "50";
        }
        else if(input.value == "sr"){
            anchorLoc = "100,200;300,200;100,600;300,600";
            roomSize = "400*800";
            // gradient = "0;3000;100";
            sampleDistance = "200";
            sigma = "50";
            maxErrShown = "10000";
            iniSeed = "roomCenter";
            customSeed = "20,20";
            dop = "all";
            count = "50";
        }
        else if(input.value == "ls"){
            anchorLoc = "1500,1500;1500,2500;2500,1500;2500,2500";
            roomSize = "4000*4000";
            // gradient = "0;3000;100";
            sampleDistance = "200";
            sigma = "50";
            maxErrShown = "10000";
            iniSeed = "roomCenter";
            customSeed = "20,20";
            dop = "all";
            count = "20";
        }
        else if(input.value == "lr"){
            anchorLoc = "1000,2000;3000,2000;1000,6000;3000,6000";
            roomSize = "4000*8000";
            
            // gradient = "0;3000;100";
            sampleDistance = "200";
            sigma = "50";
            maxErrShown = "10000";
            iniSeed = "roomCenter";
            customSeed = "20,20";
            dop = "best";
            count = "20";
        }
        else{
            anchorLoc = document.getElementById("anchorloc").value;
            roomSize = document.getElementById("roomsize").value;
            sigma = document.getElementById("sigma").value;
            // gradient = document.getElementById("gradient").value;
            sampleDistance = document.getElementById("sampledistance").value;
            maxErrShown = document.getElementById("maxerrshown").value;
            iniSeed = document.getElementById("iniseed").value;
            customSeed = document.getElementById("customseed").value;
            dop = document.getElementById("dop").value;
            count = document.getElementById("count").value;
        }
        document.getElementById("anchorloc").value = anchorLoc;
        document.getElementById("roomsize").value = roomSize;
        document.getElementById("sigma").value = sigma;
        // gradient = document.getElementById("gradient").value;
        document.getElementById("sampledistance").value = sampleDistance;
        document.getElementById("maxerrshown").value = maxErrShown;
        document.getElementById("iniseed").value = iniSeed;
        document.getElementById("customseed").value = customSeed;
        document.getElementById("dop").value = dop;
        document.getElementById("count").value = count;
    // });
    }

var totalSeconds = 0;
function validInput(){
    // var input = document.getElementById("line").value; "e.g. anchorLoc=1500,1500;1500,2500;2500,1500;2500,2500&roomSize=4000*4000&gradient=0;3000;100&sampleDistance=200&maxErrShown=10000&iniSeed=roomCenter/origin/custom&customSeed=20,20&dop=all/best"
    // var anchorLoc = document.getElementById("anchorloc").value;
    // var roomSize = document.getElementById("roomsize").value;
    // var gradient = document.getElementById("gradient").value;
    // var sample_distance = document.getElementById("sampledistance").value;
    // var maxErrShown = document.getElementById("maxerrshown").value;
    // var iniSeed = document.getElementById("iniseed").value;
    // var customSeed = document.getElementById("customseed").value;
    // var dop = document.getElementById("dop").value;

    var curWidth = parseInt(document.getElementById("contour").style.width);

    var userinput = document.getElementById("ex_inputs");
    var input_value = userinput.value;
    console.log("input_value: ");
    console.log(input_value);

    totalSeconds = 0;
    // setInterval(setTime,9000);
    setInterval(setTime,100);
    // var interval = setInterval(setTime,1000);

    progress.style.display = "block";
    tb = document.getElementById("tb"),
    progress = document.getElementById("progress"); //store these, it's better
    progress.style.width = "0%";
    function setTime(){
        ++totalSeconds;
        totalSeconds;

        // if(totalSeconds>=100) totalSeconds = 100;//keep it under 100%
        if(totalSeconds>=100) totalSeconds = 0;//go back
        // tb.text = shownProgress;// set the value of the text field     
        progress.style.width = totalSeconds+ "%";// set the width of the progress bar
        // console.log("totalseconds: ");
        // console.log(totalSeconds);
    }

    // function increase(){ 
    // //   value++;// same as value += 1, but better
    //   if(value>=100) value = 100;//keep it under 100%
    //   tb.value = shownProgress;// set the value of the text field     
    //   progress.style.width = shownProgress + "%";// set the width of the progress bar
    // } 

    if(input_value == "ss"){
        console.log("here")
        anchorLoc = "150,150;150,250;250,150;250,250";
        roomSize = "400*400";
        // gradient = "0;3000;100";
        sampleDistance = "200";
        sigma = "50";
        maxErrShown = "50";
        iniSeed = "roomCenter";
        customSeed = "20,20";
        dop = "all";
        count = "50";

        document.getElementById("anchorloc").value = anchorLoc;
        document.getElementById("roomsize").value = roomSize;
        document.getElementById("sigma").value = sigma;
        // gradient = document.getElementById("gradient").value;
        document.getElementById("sampledistance").value = sampleDistance;
        document.getElementById("maxerrshown").value = maxErrShown;
        document.getElementById("iniseed").value = iniSeed;
        document.getElementById("customseed").value = customSeed;
        document.getElementById("dop").value = dop;
        document.getElementById("count").value = count;
    }
    else if(input_value == "sr"){
        anchorLoc = "100,200;300,200;100,600;300,600";
        roomSize = "400*800";
        // gradient = "0;3000;100";
        sampleDistance = "200";
        sigma = "50";
        maxErrShown = "10000";
        iniSeed = "roomCenter";
        customSeed = "20,20";
        dop = "all";
        count = "50";

        document.getElementById("anchorloc").value = anchorLoc;
        document.getElementById("roomsize").value = roomSize;
        document.getElementById("sigma").value = sigma;
        // gradient = document.getElementById("gradient").value;
        document.getElementById("sampledistance").value = sampleDistance;
        document.getElementById("maxerrshown").value = maxErrShown;
        document.getElementById("iniseed").value = iniSeed;
        document.getElementById("customseed").value = customSeed;
        document.getElementById("dop").value = dop;
        document.getElementById("count").value = count;
    }
    else if(input_value == "ls"){
        anchorLoc = "1500,1500;1500,2500;2500,1500;2500,2500";
        roomSize = "4000*4000";
        // gradient = "0;3000;100";
        sampleDistance = "200";
        sigma = "50";
        maxErrShown = "10000";
        iniSeed = "roomCenter";
        customSeed = "20,20";
        dop = "all";
        count = "20";

        document.getElementById("anchorloc").value = anchorLoc;
        document.getElementById("roomsize").value = roomSize;
        document.getElementById("sigma").value = sigma;
        // gradient = document.getElementById("gradient").value;
        document.getElementById("sampledistance").value = sampleDistance;
        document.getElementById("maxerrshown").value = maxErrShown;
        document.getElementById("iniseed").value = iniSeed;
        document.getElementById("customseed").value = customSeed;
        document.getElementById("dop").value = dop;
        document.getElementById("count").value = count;
    }
    else if(input_value == "lr"){
        anchorLoc = "1000,2000;3000,2000;1000,6000;3000,6000";
        roomSize = "4000*8000";
        
        // gradient = "0;3000;100";
        sampleDistance = "200";
        sigma = "50";
        maxErrShown = "10000";
        iniSeed = "roomCenter";
        customSeed = "20,20";
        dop = "best";
        count = "20";

        document.getElementById("anchorloc").value = anchorLoc;
        document.getElementById("roomsize").value = roomSize;
        document.getElementById("sigma").value = sigma;
        // gradient = document.getElementById("gradient").value;
        document.getElementById("sampledistance").value = sampleDistance;
        document.getElementById("maxerrshown").value = maxErrShown;
        document.getElementById("iniseed").value = iniSeed;
        document.getElementById("customseed").value = customSeed;
        document.getElementById("dop").value = dop;
        document.getElementById("count").value = count;
    }
    else {
        anchorLoc = document.getElementById("anchorloc").value;
        roomSize = document.getElementById("roomsize").value;
        sigma = document.getElementById("sigma").value;
        // gradient = document.getElementById("gradient").value;
        sampleDistance = document.getElementById("sampledistance").value;
        maxErrShown = document.getElementById("maxerrshown").value;
        iniSeed = document.getElementById("iniseed").value;
        customSeed = document.getElementById("customseed").value;
        dop = document.getElementById("dop").value;
        count = document.getElementById("count").value;
    }

    document.getElementById("btn").disabled = true;
    // if(userinput){
    console.log("anchorLoc: ");
    console.log(anchorLoc);
    const input = "anchorLoc="+anchorLoc+"&roomSize="+roomSize+"&sampleDistance="+sampleDistance+"&sigma="+sigma+"&maxErrShown="+maxErrShown+"&iniSeed="+iniSeed+"&customSeed="+customSeed+"&dop="+dop+"&count="+count;
    console.log("input: ");
    console.log(input);
    const coors = roomSize.split("*");
    // console.log(coors);
    width = parseInt(coors[0]);
    height = parseInt(coors[1]);
    var scale = height/width;
    // gradient = gradient.split(';');
    // start = gradient[0];
    // end = gradient[1];
    // step = gradient[2];
    sample_distance = parseInt(sampleDistance);
    // console.log(inputs[1])
    const anchors = anchorLoc.split(";");
    const canvas = document.getElementById("canvas");
    var ctx = document.getElementById("canvas").getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // console.log(anchors);
    // for(var i =0; i<anchors.length;i++){
    //     const locs = anchors[i].split(",");
    //     // console.log(locs);
    //     // console.log(parseInt(locs[0])*300/width);
    //     xs.push(parseInt(locs[0])*canvasx/width);
    //     ys.push(canvasy-parseInt(locs[1])*canvasy/height);
    // }
    // console.log(xs);
    // console.log(ys);
    document.getElementById("contour").style.height = (scale*curWidth).toString()+"px";
    var pointSize = 3;


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

    const url = "http://localhost:443/path?"+input;
    // const url = "http://indoorloc-sim.cc.gatech.edu:443/path?"+input;
    var http = createCORSRequest("get", url);
    // console.log(url)
    contour_map = document.getElementById('contour');
    map = document.getElementById('map');

    http.onload = function ()
    {
        if (this.status >= 200 && this.status < 400)
        {
            var data = JSON.parse(this.response);
            console.log(data);
            var x_axis = [];
            for (var i = 0; i <= width/1000;i = i+sample_distance/1000) {
                // console.log(i);
                x_axis.push(i);
            }
            var y_axis = [];
            for (var i = 0; i <= height/1000;i = i+sample_distance/1000) {
                y_axis.push(i);
            }
            var contour_data = [{
                z: data,
                type: 'contour',
                // colorscale:{range: [0,10000]},
                // colorscale:"Jet",
                x: x_axis,
                y: y_axis,
                // contours : {
                //     start :start,
                //     end :end,
                //     size :step},
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
                width: 500*(width/height),
                height: 500,
                title: 'Colorscale for Contour Plot',
                automargin: false,

                xaxis:{range: [0,width/1000]},
                yaxis:{range: [0,height/1000]},
                // coloraxis:{colorbar: {dtick:0.1}},
            }
            Plotly.newPlot(contour_map, contour_data, layout);
            // console.log(data);

            // for (var i = 0; i< xs.length; i++){
            //     console.log('reach here')
            //     getPosition(xs[i],ys[i]);
            // }
            // xs = [];
            // ys = [];
            document.getElementById("btn").disabled = false;
            // progress.style.width = "100%";
            progress.style.display = "none";
            // totalSeconds = 100;
        } else
        {
            // We reached our target server, but it returned an error.
            console.log("Error status not between 200 and 400.");
        }
    };
// console.log("gethere");
    http.onerror = function (e)
    {
        // There was a connection error of some sort.
        console.log(e);
    };

    http.send();

    // document.querySelector('btn').disabled = false;
    // document.addEventListener("DOMContentLoaded", function(event) {
    // document.getElementById("btn").disabled = false;

    //     console.log("set btn to false");
    //   });
    // console.log("to the end")
    // totalSeconds = 100;
}