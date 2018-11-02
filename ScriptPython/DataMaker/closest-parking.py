import numpy as np
import math
import time
import folium
import random
dts = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/data_by_parking_2.npy')

coupleParking = []
print(dts[0])


def traitement(line1,line2,tab):
    l11 = (math.pi*line1[1])/180.0
    l12 = (math.pi*line1[2])/180.0
    l21 = (math.pi*line2[1])/180.0
    l22 = (math.pi*line2[2])/180.0
    val = float(math.sin(l12)*math.sin(l22) + math.cos(l12)*math.cos(l22)*math.cos(l21 - l11))

    if (val < -1 or val > 1):

        if val < 0:
            val = -1
        else:
            val = 1

    dist = (180/math.pi)*math.acos(val)*60*1852
    dist = dist/1.41

    if (dist < 100 and abs(line1[3]-line2[3])>1):
        #print("hourly rate : ",line1[3]," vs ",line2[3]," || distance : ",dist)
        id1 = line1[0]
        id2 = line2[0]
        x1 = line1[1]
        x2 = line2[1]
        y1 = line1[2]
        y2 = line2[2]
        t = [id1,id2,x1,y1,x2,y2]
        tab.append(t)

#cpt=0
#N = len(dts)
#for line1 in dts:
    #cpt+=1
    #if cpt%250 == 0:
        #print("still computing line ",cpt,"/",N," ...")
    #for line2 in dts:
        #traitement(line1,line2,coupleParking)


couple = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple.npy')
print("nombre de couple : ",len(couple))
N = len(couple)
tab_coordinate = []
cpt = 0
for line in couple:
    cpt+=1
    if cpt%10000 == 0:
        print("still computing line ",cpt,"/",N," ...")
    coord1 = [line[2],line[3]]
    coord2 = [line[4],line[5]]
    if coord1 not in tab_coordinate:
        tab_coordinate.append(coord1)
    if coord2 not in tab_coordinate:
        tab_coordinate.append(coord2)

color = ['#9F258A' , '#58184D' , '#D8246B' , '#D82434' , '#82373E'  , '#7C7FAD'  , '#333FC9'  , '#0010D6'  , '#00D6AF'  , '#368C7D'  , '#3F8C36' , '#1AF900' ,'#F5F900'  ,'#F98000']

map_osm = folium.Map(location=[48.711478,2.207708])
print(" starting the creation of the map ")

for i in range(0,len(tab_coordinate)-1,2):

    coord1 = tab_coordinate[i]
    coord2 = tab_coordinate[i+1]
    indx = random.randint(0,13)
    col = color[indx]
    name = "parking"+" "+str(i)
    map_osm.add_child(folium.RegularPolygonMarker(location=coord1, popup=name,fill_color=col, radius=5))
    map_osm.add_child(folium.RegularPolygonMarker(location=coord2, popup=name,fill_color=col, radius=5))


print("map created")

map_osm.save('parking-map-couple.html')

#print(len(coupleParking))
print("done")


#np.save('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/parking-couple',coupleParking)
