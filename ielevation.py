import urllib3
import re
import pandas as pd
import math
import numpy as np
from circular_locations import straightlines
import time
import sys

#start_lat = sys.argv[1]
#start_long = sys.argv[2]

def retreive_html_elevation(lat):
    response = urllib3.request("GET", "https://api.opentopodata.org/v1/eudem25m?locations=" + lat)
    response = response.data
    response = response.decode()
    results = re.findall("      \"elevation\": (\d+)\.\d+,", response)


    return results

# These are the only arguments to parse
df = straightlines(start_lat = 60.3268384, start_lon=	
9.4876382, r_value=0.005)

## Need to split the dataframe into parts of length 100 or less

def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier


lat_string = ""
for i in np.arange(start = 0, stop = round_up(len(df.index)/100), step = 1):
     temp_df = df.iloc[int(i)*100:(int(i)+1)*100]
     for j in range(len(temp_df)):
        lat_string += str(temp_df.iloc[j][0])
        lat_string += ","
        lat_string += str(temp_df.iloc[j][1])
        if j < len(temp_df)-1:
            lat_string += "|"
        if j == len(temp_df)-1:
            lat_string += "split"
        
split_lat_string = lat_string.split("split")
del split_lat_string[len(split_lat_string)-1]

# This is where the actual elevation data is retreived
coord_elevation_df = pd.DataFrame({'latlon':[], 'elevation':[]})
for i in split_lat_string:
    latlon_list = i.split("|")
    #print(len(latlon_list))
    elevation_list = retreive_html_elevation(i)

    test_df = pd.DataFrame({'latlon':latlon_list, 'elevation':elevation_list})
    coord_elevation_df = pd.concat([coord_elevation_df, test_df])


# Spliting the lonlat column into two columns
coord_elevation_df[["lat", "lon"]] = coord_elevation_df["latlon"].str.split(",", expand = True)
coord_elevation_df = coord_elevation_df.drop(columns= ["latlon"])
coord_elevation_df.to_csv("coord_elevation_df2.csv")
print(coord_elevation_df)
