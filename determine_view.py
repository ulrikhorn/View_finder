#!/home/ulrik/mambaforge/envs/python/bin/python

import urllib3
import re
import pandas as pd
import math
import numpy as np
from circular_locations import straightlines
import time
import folium
from geopy import distance

df = pd.read_csv("coord_elevation_df2.csv")
angles = list(np.arange(0,36,1))*int(len(df)/36)

itterations = np.array([np.arange(0, len(df)/36)])
itterations = np.repeat(itterations, 36)

df = df.assign(angle = angles)
df = df.assign(itteration = itterations)

initial_elevation = int(df.iloc[0][1])



#Are the datapoints higher or lower than the viewpoint elevationls

# Mutating columns conditionally (Mutate ifelse in R)
df = df.assign(lower = ['true' if i < initial_elevation else 'false' for i in df['elevation']])


# Getting the distance to start for geometry calcs
dist_list = []
for i in range(len(df)):
    point1 = (df.loc[1]['lat'], df.loc[1]['lon'])
    point2 = (df.loc[i]['lat'], df.loc[i]['lon'])
    dist = str(distance.geodesic(point1, point2, ellipsoid = 'GRS-80').m)
    dist  = re.findall('\d+\.\d+', dist)
    dist_list.append(*dist)
    
df= df.assign(distance_to_start = dist_list)

height_diff = []
for i in range(len(df)):
    elev_diff = df.loc[i]['elevation'] - df.loc[1]['elevation']
    height_diff.append(elev_diff)

df = df.assign(elev_diff = height_diff)    

hypotenuse = []
for i in range(len(df)):
    kat1 = df.loc[i]['elev_diff']
    kat2 = df.loc[i]['distance_to_start']
    #print(type(kat2))
    kat1 = int(float(kat1))
    kat2 = int(float(kat2)) 
    hyp = math.sqrt((kat1**2)+(kat2**2))
    if df.loc[i]['elev_diff'] > 0:
        hypotenuse.append(hyp)
    else:
        hypotenuse.append(0)

df = df.assign(hyp = hypotenuse)

df = df.assign(angle_degrees= np.arcsin(elev_diff/hyp))
df = df.assign(angle_degrees= [np.arcsin(elev_diff/hyp) if i > 0 else 0 for i in df['elev_diff']])

print(df)












map = folium.Map(location = [61.0349, 7.8862], zoom_start = 10)


# folium.CircleMarker(location=[df.lat, df.lon],
#                         radius=2,
#                         weight=5).add_to(map)


latlon = []
for i in range(len(df)):
    latlon.append([df.loc[i]['lat'], df.loc[i]['lon']])

mapit = folium.Map( location=[61.0349, 7.8862], zoom_start=6 )
for coord in latlon:
    folium.Marker( location=[ coord[0], coord[1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )

mapit.save( 'map.html')

output_file = "map.html"
mapit.save(output_file)





