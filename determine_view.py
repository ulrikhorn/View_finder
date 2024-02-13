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

df = df.assign(angle_nr = angles)
df = df.assign(itteration = itterations)

initial_elevation = int(df.iloc[0][1])



#Are the datapoints higher or lower than the viewpoint elevationls

# Mutating columns conditionally (Mutate ifelse in R)
df = df.assign(lower = ['true' if i < initial_elevation else 'false' for i in df['elevation']])
df.loc[:35, 'lower'] = 'start'

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

df['angle'] = np.arcsin(df['elev_diff']/df['hyp'])
#df = df.assign(angle=lambda x: np.arcsin(x.elev_diff/x.hyp))
#df['angle'] = df.apply(lambda row: np.arcsin(row.elev_diff/row.hyp, axis=1))

#df = df.assign(angle= [(elev_diff/hyp) if i > 0 else 0 for i in df['elev_diff']])
#df.columns.values[0] = ['index']
#print(df)
#print(df.iloc[df.groupby('angle_nr',)['elevation'].idxmax()])

#print(df)

## Function to find height given angle and length
def height_at(dist_to_start, angle_at_query):
    c = (dist_to_start/math.cos(angle_at_query))
    height = math.sqrt((c**2)-(dist_to_start**2))
    return height


df = df.rename(columns={'Unnamed: 0' : 'nr'})

df['highest_seen'] = 'FALSE'
df['seen'] = 'FALSE'

for i in np.unique(df['angle_nr']):
    highest_seen = df.query(f'angle_nr == {i} & lower == "false"') # this should be the first row where lower = false
    for j in np.unique(df['itteration']):
        if int(j) < 39: # this needs to be spesific for number of itterations
            query_itt = df.query(f'angle_nr == {i} & itteration == {j}')
            if int(query_itt['itteration']) == 0:
                    df['seen'][int(query_itt['nr'])] = "true"
                    continue
            else:
                if query_itt['lower'].to_string(index=False) == 'false': # and this is the first lower == false
                    highest_seen = query_itt
                else:
                    if query_itt['lower'].to_string(index=False) == 'false':
                        if int(query_itt['elevation']) > int(highest_seen['elevation']):
                            #print(height_at(float(highest_seen['distance_to_start']), float(query_itt['angle'])))
                            if height_at(float(highest_seen['distance_to_start']), float(query_itt['angle'])) < int(query_itt['elev_diff']):
                                print("test3")
                                highest_seen = query_itt

            df['highest_seen'][int(highest_seen['nr'])] = "true"
            print("done")
        else:
            

            else:
                
                            
                            #print(query_itt['nr'])

                

#if j == max(np.unique(df['itteration'])):
# test = df.query('angle_nr == 1 & itteration == 1')
# df['highest_seen'][int(test['nr'])] = "true"
#print(df)

print(df)
# latlon= [float(df.query('highest_seen == "true"')['lat']), float(df.query('highest_seen == "true"')['lon'])]
# print(latlon)
df.to_csv("df.csv")








# folium.CircleMarker(location=[df.lat, df.lon],
#                         radius=2,
#                         weight=5).add_to(map)


latlon = []
for i in range(len(df)):
    if df.loc[i]['highest_seen'] == 'true' or df.loc[i]['itteration'] == 0 or df.loc[i]['seen'] == 'true':
        latlon.append([df.loc[i]['lat'], df.loc[i]['lon']])


mapit = folium.Map( location=[60.3268384, 9.4876382], zoom_start=12 )
for coord in latlon:
    folium.Marker( location=[ coord[0], coord[1] ], fill_color='#43d9de', radius=8 ).add_to( mapit )

mapit.save( 'map2.html')

output_file = "map2.html"
mapit.save(output_file)





