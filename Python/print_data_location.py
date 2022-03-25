# -*- coding: utf-8 -*-
"""
Created on Thu Oct 14 16:27:03 2021

@author: TIAGO
"""

import json
import dateutil.parser as dp
from collections import defaultdict
import utm
import numpy as np
# import matplotlib.pyplot as pltX
# import matplotlib.pyplot as pltY
# import matplotlib.pyplot as pltXY


devices_dict = defaultdict(list) #dictionary of lists where key = {device} and value = {time_gps}
gps_dict = defaultdict(list)
munster_gps = defaultdict(list)
munster_dictX = defaultdict(list)
munster_dictY = defaultdict(list)

tripsX = []
tripsY = []
lat = []
long = []
diff = []
key_aux = ""
diff_list = []
fp = open("MUNSTER256.txt",'w')


#%%

def checkCell(x, y, n):
     j = 1
     #cell = 0
     x_aux = 0
     y_aux = 0
     
     diffX = max(tripsX) - min(tripsX) #length
     diffY = max(tripsY) - min(tripsY) #width
     
     cellX = diffX/n #length of a cell in x
     cellY = diffY/n #width of a cell in y
     
     dX = np.floor((x - min(tripsX)) / (cellX+0.0000001))
     dY = np.floor((y - min(tripsY)) / (cellY+0.0000001))
       
     cell = np.int((dX + 1) + n*dY)
       
     return cell
     #print(cellX)
     #print(cellY)
     
     #area = cellX * cellY
     #print(area)
        
     # while j <= n:
     #   y_aux = min(tripsY) + j*cellY
     #   k = n+1
      
     #   for i in range(1, k): #cycle through the length of the grid in x
     #       x_aux = min(tripsX) + i*cellX
     #       cell+=1
          
     #       if x <= x_aux and y <= y_aux:
     #           return cell
     #       # else:
     #       #     cell+=1
           
      
     #   j+=1
    

#%% 
## treat the raw data as a JSON object
with open("location.geojson") as f:
    data = json.load(f)
    
#file = open("musnter_data.txt", "w")

for feature in data['features']:
    key = feature['properties']['device'] # key is the name of the device
    
    
    devices_dict[key].append(feature['properties']['time_gps']) # for each name of the device we get the respective time of the gps
    gps_dict[key].append(feature['geometry']['coordinates'])    

    


#%%
#handle the gps coordinates and converts them to cartesian
k = 0              
for key, values in gps_dict.items():
    k = 0
    for value in values:
        lat_aux = round(value[0], 2)
        long_aux = round(value[1], 2)
          
        if (lat_aux >= 7.57 and lat_aux <= 7.66) and (long_aux >= 51.92 and long_aux <= 51.99): #approx the lat,long of munster
            #munsterGPS(key, key_aux, k)
            munster_gps[key].append(devices_dict[key][k])
            x, y, zone, ut = utm.from_latlon(lat_aux, long_aux)
            tripsX.append(x)
            tripsY.append(y)
            munster_dictX[key].append(x)
            munster_dictY[key].append(y)
        k+=1 
                   


#%%
t2 = 0.0        
j = 0        
    
for key, values in munster_gps.items():
    j = 0
    for value in values:
            str_aux = str(value)
            #print(j)
            string_aux1 = str_aux.replace('[', '')
            string_aux2 = string_aux1.replace(']','')
            parsed_t = dp.parse(string_aux2)
            t1 = parsed_t.timestamp()
            #print(t1)
            diff_aux = float(t1 - t2)
            t2 = t1 # t2 is the current time and t1 is the next time
            diff.append(diff_aux)
            
            if diff_aux > 30:
                if diff_aux > 300: #new trip 
                    cell = checkCell(munster_dictX[key][j], munster_dictY[key][j], 16)
                    #trajectorySeq.append(cell)
                    fp.write('\n' + str(cell) + ' ')
                else:
                    cell = checkCell(munster_dictX[key][j], munster_dictY[key][j], 16)
                    #trajectorySeq.append(cell)
                    fp.write(str(cell) + ' ')
            j+=1

#%%
# print(max(tripsX))
# print(min(tripsX)) #XDIFF - 7741; 1935
# print(max(tripsY))
# print(min(tripsY)) #YDIFF - 9958; 2489
# #print(max(lat))
# #print(min(lat))
# #print(max(long))
# #print(min(long))        
# #print(histoX, histoY)   
# #pltX.hist(histoX, bins=10, label = 'latitude')
# pltXY.plot(tripsX, tripsY, 'r.')
#pltX.legend()
#pltX.show()
#pltY.hist(histoY, bins=10, label = 'longitude')
#pltY.legend()
#pltX.show()
#%%
fp.close()
