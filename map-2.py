import folium
import numpy as np
from pyensae.notebookhelper import folium_html_map

def read_coordinate(s):
    sx = ""
    sy = ""
    cpt = 0
    while s[cpt] != ",":
        sx += s[cpt]
        cpt+=1
    sy = s[cpt+1:]
    #print("test x : ",sx)
    #print("test y : ",sy)
    x = float(sx)
    y = float(sy)
    return x,y
print("start loeading data...")
dts0 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_0.npy')
dts1 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_1.npy')
dts2 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_2.npy')
dts3 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_3.npy')
dts4 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_4.npy')
dts5 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_5.npy')
print("data loaded")
tab_coordinate = []
print("start computing from dstet0...")
for data in dts0:
    coord = data[12]
    x,y = read_coordinate(coord)
    c = [x,y]
    if c not in tab_coordinate:
        tab_coordinate.append(c)
print("start computing from dstet1...")

for data in dts1:
    coord = data[12]
    x,y = read_coordinate(coord)
    c = [x,y]
    if c not in tab_coordinate:
        tab_coordinate.append(c)
print("start computing from dstet2...")

for data in dts2:
    coord = data[12]
    x,y = read_coordinate(coord)
    c = [x,y]
    if c not in tab_coordinate:
        tab_coordinate.append(c)
print("start computing from dstet3...")

for data in dts3:
    coord = data[12]
    x,y = read_coordinate(coord)
    c = [x,y]
    if c not in tab_coordinate:
        tab_coordinate.append(c)
print("start computing from dstet4...")

for data in dts4:
    coord = data[12]
    x,y = read_coordinate(coord)
    c = [x,y]
    if c not in tab_coordinate:
        tab_coordinate.append(c)
print("start computing from dstet5...")

for data in dts5:
    coord = data[12]
    x,y = read_coordinate(coord)
    c = [x,y]
    if c not in tab_coordinate:
        tab_coordinate.append(c)

print("all points computed ",len(tab_coordinate)," points")

map_osm = folium.Map(location=[48.711478,2.207708])
print(" starting the creation of the map ")
for i in range(len(tab_coordinate)):
    coord = tab_coordinate[i]
    name = "parking"+" "+str(i)
    print(name," coordinates being : ",coord)
    map_osm.add_child(folium.RegularPolygonMarker(location=coord, popup=name,fill_color='#132b5e', radius=4))

print("map created")
#from IPython.display import HTML
#HTML(folium_html_map(map_osm))
map_osm.save('parking-map-basique.html')
