import numpy as np
import folium
import os
import branca
import pandas as pd
#from pyensae.notebookhelper import folium_html_map
from branca.utilities import split_six

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



#colorscale = branca.colormap.linear.YlGnBu_09.scale(0, 30)
employed_series = geoArrondissement

#style_function = lambda x: {'fillColor': colorscale(x['properties']['avgTime'])}

map_osm = folium.Map(tiles='Stamen Toner',location=[48.711478,2.207708])






map_osm.choropleth(geo_data=geoArrondissement, data=df,
              columns=['objectid','avgCost'],
              key_on='feature.properties.objectid',
              fill_color='BuPu',
              name = 'avgCost',
              threshold_scale=[1.8,2.3,2.7,3.4,3.7,4.1],
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='Cout du parking en moyenne (euro)',
              highlight=True)

map_osm.choropleth(geo_data=geoArrondissement, data=df,
              columns=['objectid','ratioCB'],
              key_on='feature.properties.objectid',
              fill_color='YlGn',
              name = 'ratioCB',
              threshold_scale=[0.40,0.425,0.45,0.47,0.49,0.52],
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='Taux de payments CB',
              highlight=True)

map_osm.choropleth(geo_data=geoArrondissement, data=df,
              columns=['objectid','ratioRot'],
              key_on='feature.properties.objectid',
              fill_color='YlOrRd',
              name = 'ratioROT',
              threshold_scale=[0.73,0.76,0.78,0.81,0.84,0.87],
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='Taux dutilisateurs rotatifs',
              highlight=True)

map_osm.choropleth(geo_data=geoArrondissement, data=df,
              columns=['objectid','count'],
              key_on='feature.properties.objectid',
              fill_color='YlOrRd',
              name = 'avgCount',
              threshold_scale=[219,223.25,227.5,231.75,236,238],
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='Nombre utilisateurs moyens',
              highlight=True)

map_osm.choropleth(geo_data=geoArrondissement, data=df,
              columns=['objectid','avgTime'],
              key_on='feature.properties.objectid',
              fill_color='PuBu',
              name = 'avgTime',
              threshold_scale=[6,7,7.5,8,9,10],
              fill_opacity=0.7,
              line_opacity=0.2,
              legend_name='Temps passé sur parking en moyenne (Heure)',
              highlight=True)

folium.GeoJson(geoOtherParking,name='geojsonParking').add_to(map_osm)

folium.LayerControl().add_to(map_osm)

print("map created")
#from IPython.display import HTML
#HTML(folium_html_map(map_osm))
map_osm.save('arrondissement-map-test-bis.html')
