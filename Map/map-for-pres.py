import numpy as np
import folium
import os
import branca
import pandas as pd
from pyensae.notebookhelper import folium_html_map
from branca.utilities import split_six
import random 
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
print("=>")
dts0 = np.load('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data/t_and_l_full_0.npy')
print("===>")
print("data loaded")

######################

geoArrondissement = os.path.join('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data', 'arrondissements.geojson')
dataArrondissement = os.path.join('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data', 'arrondissement-data.csv')
geoOtherParking = os.path.join('/Users/paulgarnier/Desktop/Files/GitHub/datacaseOW/data', 'parcs-de-stationnement-concedes-de-la-ville-de-paris.geojson')
df = pd.read_csv(dataArrondissement)

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


#colorscale = branca.colormap.linear.YlGnBu_09.scale(0, 30)
employed_series = geoArrondissement

#style_function = lambda x: {'fillColor': colorscale(x['properties']['avgTime'])}

map_osm = folium.Map(location=[48.711478,2.207708])


map_osm.choropleth(geo_data=geoArrondissement, data=df,
              columns=['objectid','hrate'],
              key_on='feature.properties.objectid',
              fill_color='Paired',
              name = 'hrate',
              threshold_scale=[2,3,4],
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='h_rate',
              highlight=True)

for i in range(0,len(tab_coordinate)-1,2):

    coord1 = tab_coordinate[i]
    coord2 = tab_coordinate[i+1]
    indx = random.randint(0,13)
    col = color[indx]
    name = "parking"+" "+str(i)
    map_osm.add_child(folium.RegularPolygonMarker(location=coord1, popup=name,fill_color=col, radius=5))
    map_osm.add_child(folium.RegularPolygonMarker(location=coord2, popup=name,fill_color=col, radius=5))



#folium.GeoJson(geoOtherParking,name='geojsonParking').add_to(map_osm)

folium.LayerControl().add_to(map_osm)

print("map created")
#from IPython.display import HTML
#HTML(folium_html_map(map_osm))
map_osm.save('/Users/paulgarnier/Desktop/Files/arrondissement-map-test-bis.html')
