import urllib.request
import re
import pandas as pd
import math
import numpy as np
from circular_locations import straightlines

# Use opentopodata to retreive elevation data
def retreive_html_elevation(lat, lon):
    with urllib.request.urlopen(
            "https://amath.pi.opentopodata.org/v1/eudem25m?locations=" + lat + "," + lon) as response:
        html = response.read()
    results = html.decode()
    results = re.findall("      \"elevation\": (\d+)\.\d+,", results)


    return results



df = straightlines(start_lat = 61.0349, start_lon=7.8862, r_value=0.01)

print(df)


## Need to split the dataframe into parts of length 100 or less


def round_up(n, decimals=0):
    multiplier = 10**decimals
    return math.ceil(n * multiplier) / multiplier

#Test
# for i in range(round_up(len(df.index)/100)):
#     print(i)
#     lat = df.iloc[i][0]
#     lon = df.iloc[i][1]
#     if i < 100:
#         print(lon, lat)