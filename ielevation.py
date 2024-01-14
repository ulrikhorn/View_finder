import urllib3
import re
import pandas as pd
import math
import numpy as np
from circular_locations import straightlines
import time


def retreive_html_elevation(lat, lon):
    response = urllib3.request("GET", "https://api.opentopodata.org/v1/eudem25m?locations=" + lat + "," + lon)
    response = response.data
    response = response.decode()
    results = re.findall("      \"elevation\": (\d+)\.\d+,", response)


    return results


df = straightlines(start_lat = 61.0349, start_lon=7.8862, r_value=0.01)


## Need to split the dataframe into parts of length 100 or less


def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier


lat_string = ""
lon_string = ""
for i in np.arange(start = 0, stop = round_up(len(df.index)/100), step = 1):
     temp_df = df.iloc[int(i)*100:(int(i)+1)*100]
     #print(temp_df)
     for j in range(len(temp_df)):
        lat_string += str(temp_df.iloc[j][0])
        lat_string += ","
        lat_string += str(temp_df.iloc[j][1])
        if j < len(temp_df):
            lat_string += "|"
        print(lat_string)
