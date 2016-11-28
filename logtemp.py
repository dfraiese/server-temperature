#!/usr/bin/env python
# -*- coding: utf-8
#!/usr/bin/python

import datetime

def sensores():
    import sensors
    import sys

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
        
    return v_temp, v_cooler

if __name__ == "__main__":
    temp, cooler = sensores()
    
    print str(datetime.datetime.now())[0:19] + repr(temp).rjust(10) + repr(cooler).rjust(10)

