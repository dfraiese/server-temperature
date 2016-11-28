# -*- coding: utf-8 -*-

import sys
import datetime
from datetime import timedelta
from dateutil import parser

def open_file(path, modo):
    try:
        file = open(path, modo)
    except Exception, e:
        print str(datetime.datetime.now()) + "-" + "ERROR " + "-" + str(e)
        sys.exit()
    else:
        return file

def close_file(file):
    try:
        file.close()
    except Exception, e:
        print str(datetime.datetime.now()) + "-" + "ERROR " + "-" + str(e)
        sys.exit()

def read_logtemp(sPath, opcion):
    l_temp_x = []
    l_temp_y = []
    l_cooler_x = []
    l_cooler_y = []
    
    s_temp_x = "" 
    s_temp_y = ""
    s_cooler_x = "" 
    s_cooler_y = ""
    
    k = 1
    
    dt_now = datetime.datetime.now()
    f = open_file(sPath, "r")
    
    for l in f:
        dt = parser.parse(l[0:19])

        if dt > dt_now-timedelta(hours=24):
            l_temp_x.append('"' + l[0:19][10:16] + '"') 
            l_temp_y.append(str(int(float(l[20:29]))))
            
            l_cooler_x.append('"' + l[0:19][10:16] + '"')
            l_cooler_y.append(str(int(float(l[31:39]))))
            
    j = 0
    for i in l_temp_x:   
        if k < len(l_temp_x):
            s_temp_x = s_temp_x + l_temp_x[j] + ","
            s_temp_y = s_temp_y + l_temp_y[j] + ","
        else:
            s_temp_x = s_temp_x + l_temp_x[j]
            s_temp_y = s_temp_y + l_temp_y[j]
            
        k = k + 1
        j = j + 1
        
    k = 1
    j = 0
    for i in l_cooler_x:
        if k < len(l_cooler_x):
            s_cooler_x = s_cooler_x + l_cooler_x[j] + ","
            s_cooler_y = s_cooler_y + l_cooler_y[j] + ","
        else:
            s_cooler_x = s_cooler_x + l_cooler_x[j]
            s_cooler_y = s_cooler_y + l_cooler_y[j]
            
        k = k + 1
        j = j + 1
    
    close_file(f)
    
    s_temp_x = "[" + s_temp_x + "]"
    s_temp_y = "[" + s_temp_y + "]"
    
    s_cooler_x = "[" + s_cooler_x + "]"
    s_cooler_y = "[" + s_cooler_y + "]"
    
    s_temp_x = s_temp_x.replace(" ", "")
    s_temp_y = s_temp_y.replace(" ", "")
    
    s_cooler_x = s_cooler_x.replace(" ", "")
    s_cooler_y = s_cooler_y.replace(" ", "")
    
    if opcion == "tempx":
        return s_temp_x 
    
    if opcion == "tempy":
        return s_temp_y 
    
    if opcion == "coolerx":
        return s_cooler_x 

    if opcion == "coolery":
        return s_cooler_y 

def sensores():
    import sensors

    sensors.init()

    l_div = []

    i = 1
    v_temp = 0
    v_cooler = 0
    
    d_chip = {}
    
    try:
        for chip in sensors.iter_detected_chips():
            for feature in chip:
                label = feature.label
                valor = str(feature.get_value())
                
                l_chip = []
                d_chip.setdefault(feature.name, l_chip)
                
                l_chip.append(i)
                l_chip.append(label)
                l_chip.append(valor)
                                                
                i = i + 1
    except Exception, e:
        return str(datetime.datetime.now()) + "-" + "ERROR SENSORES" + "-" + str(e)
    finally:
        sensors.cleanup()
        
    div = []
    n = len(d_chip)
    k = 1
    m = 0
    
    valorMax = 0
    
    l_valorAux = []
        
    for j in d_chip:
        labelTag = j
        valorTag = d_chip[j][2]
        
        if valorTag not in l_valorAux:
            l_valorAux.append(valorTag)
            
            if labelTag.find("temp") != -1:
               if "temp23" in labelTag:
                   if valorTag > valorMax:
                      valorMax = valorTag
                      labelMax = labelTag

		      v_temp = float(valorMax)

		      k = k + 1
            else:
               m = m + 1
            
    if m > 0:
        v_cooler = float(valorTag)

        html_00 = """ 
        <head>
	  <!-- Plotly.js -->
	  <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
          <script src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script>
          <script>
              function cicle() {
                  cooler();
                  temp();
		  histogram();
              }
              $(document).ready(function () { setInterval(cicle, 2000); });
        </script>
	</head>

	<body onload="cicle()"> 
	  <div id="Div03" style="width: 640px; height: 400px; float: left;"></div>
	  <div id="Div01" style="width: 400px; height: 400px; float: left;"></div>
	  <div id="Div02" style="width: 400px; height: 400px; float: left;"></div>
	  <div id="Div04" style="width: 640px; height: 400px; float: left;"></div>
	  <script>
              function cooler() {
		""" + "var level = " + str(v_cooler) + ";" + """
                var levelAux = (level / 4500) * 180
		// Trig to calc meter point
		var degrees = 180 - levelAux,
	        radius = .5;
		var radians = degrees * Math.PI / 180;
		var x = radius * Math.cos(radians);
		var y = radius * Math.sin(radians);

		// Path: may have to change to create a better triangle
		var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
		     pathX = String(x),
		     space = ' ',
		     pathY = String(y),
		     pathEnd = ' Z';
		var path = mainPath.concat(pathX,space,pathY,pathEnd);

		var data = [{ type: 'scatter',
		   x: [0], y:[0],
		    marker: {size: 28, color:'850000'},
		    showlegend: false,
		    name: 'speed',
		    text: level,
		    hoverinfo: 'text+name'},
		  { values: [4500/6, 4500/6, 4500/6, 4500/6, 4500/6, 4500/6, 4500],
		  rotation: 90,
		  text: ['TOO FAST!', 'Pretty Fast', 'Fast', 'Average',
	        	    'Slow', 'Super Slow', ''],
		  textinfo: 'text',
		  textposition:'inside',      
		  marker: {colors:['rgb(237, 0, 0)', 'rgb(237, 118, 0)',
	                         'rgb(237, 237, 0)', 'rgb(0, 237, 0)',
	                         'rgb(213, 237, 213)', 'rgb(167, 186, 167)',
	                         'rgb(255, 255, 255)']},
		  labels: ['3751-4500', '3001-3750', '2251-3000', '1501-2250', '751-1500', '0-750', ''],
		  hoverinfo: 'label',
		  hole: .5,
		  type: 'pie',
		  showlegend: false
		}];

		var layout = {
		  shapes:[{
		      type: 'path',
		      path: path,
		      fillcolor: '850000',
	      	line: {
	        	color: '850000'
		      }
		    }],
		  title: '<b>Cooler</b> <br> Speed 0-4500',
		  height: 400,
		  width: 400,
		  xaxis: {zeroline:false, showticklabels:false,
	        	     showgrid: false, range: [-1, 1]},
		  yaxis: {zeroline:false, showticklabels:false,
		             showgrid: false, range: [-1, 1]}
		};

		Plotly.newPlot('Div01', data, layout);
             }
	  </script>
	  <script>
	     function temp() {
		""" + "var level = " + str(v_temp) + ";" + """
                var levelAux = (level / 100) * 180 
		// Trig to calc meter point
		var degrees = 180 - levelAux,
		     radius = .5;
		var radians = degrees * Math.PI / 180;
		var x = radius * Math.cos(radians);
		var y = radius * Math.sin(radians);

		// Path: may have to change to create a better triangle
		var mainPath = 'M -.0 -0.025 L .0 0.025 L ',
		     pathX = String(x),
		     space = ' ',
		     pathY = String(y),
		     pathEnd = ' Z';
		var path = mainPath.concat(pathX,space,pathY,pathEnd);

		var data = [{ type: 'scatter',
		   x: [0], y:[0],
		    marker: {size: 28, color:'850000'},
		    showlegend: false,
		    name: 'degrees',
		    text: level,
		    hoverinfo: 'text+name'},
		  { values: [100/6, 100/6, 100/6, 100/6, 100/6, 100/6, 100],
		  rotation: 90,
		  text: ['TOO HOT!', 'Pretty hot', 'hot', 'Average',
	        	    'cold', 'very cold', ''],
		  textinfo: 'text',
		  textposition:'inside',      
		  marker: {colors:['rgb(237, 0, 0)', 'rgb(237, 118, 0)',
	                         'rgb(237, 237, 0)', 'rgb(0, 237, 0)',
	                         'rgb(213, 237, 213)', 'rgb(167, 186, 167)',
	                         'rgb(255, 255, 255)']},
		  labels: ['88-100', '70-87', '53-69', '35-52', '18-34', '0-17', ''],
		  hoverinfo: 'label',
		  hole: .5,
		  type: 'pie',
		  showlegend: false
		}];

		var layout = {
		  shapes:[{
		      type: 'path',
		      path: path,
		      fillcolor: '850000',
		      line: {
	        	color: '850000'
		      }
		    }],
		  title: '<b>Temperature</b> <br> 0-100 degrees',
		  height: 400,
		  width: 400,
		  xaxis: {zeroline:false, showticklabels:false,
	        	     showgrid: false, range: [-1, 1]},
		  yaxis: {zeroline:false, showticklabels:false,
		             showgrid: false, range: [-1, 1]}
		};

		Plotly.newPlot('Div02', data, layout);
             }
	  </script>
         <script>
		function histogram() {
	   	 var trace1 = {
		  x: """ + read_logtemp("/home/diego/logtemp.cvs", "tempx") + """,
		  y: """ + read_logtemp("/home/diego/logtemp.cvs", "tempy") + """,
		  mode: 'lines',
		  name: 'Temperature'
		};

		var trace2 = {
		  x: """ + read_logtemp("/home/diego/logtemp.cvs", "coolerx") + """,
		  y: """ + read_logtemp("/home/diego/logtemp.cvs", "coolery") + """,
		  mode: 'lines',
                  name: 'Cooler'
		};

		var layout_cooler = {
                        title:'Cooler'
		};

		var layout_temp = {
                        title:'Temperature',
			  yaxis: {
			    autorange: true
			  }
		};

		Plotly.newPlot('Div03', [ trace1 ], layout_temp); 
        	Plotly.newPlot('Div04', [ trace2 ], layout_cooler);
	  }
	</script>
	</body>
	"""

    l_div.append(html_00)
 
    return l_div


def application(environ, start_response):
    respuesta = sensores() 
    #respuesta = "<p>" + "hola" + str(environ["PATH_INFO"]) + "</p>"
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return respuesta




