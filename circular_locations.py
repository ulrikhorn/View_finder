#circular_locations.py
#test
import pandas as pd
import math
import numpy as np

def straightlines(start_lat, start_lon, r_value):
    df = pd.DataFrame({'lat':[], 'lon':[]})

    for r in np.arange(0,0.2, r_value):
        lon_list = [start_lon+r*math.cos(10*math.pi/180),
        start_lon+r*math.cos(20*math.pi/180),
        start_lon+r*math.cos(math.pi/6),
        start_lon+r*math.cos(40*math.pi/180),
        start_lon+r*math.cos(50*math.pi/180),
        start_lon+r*math.cos(math.pi/3),
        start_lon+r*math.cos(70*math.pi/180),
        start_lon+r*math.cos(80*math.pi/180),
        start_lon+r*math.cos(math.pi/2),
        start_lon+r*math.cos(100*math.pi/180),
        start_lon+r*math.cos(110*math.pi/180),
        start_lon+r*math.cos(2*math.pi/3),
        start_lon+r*math.cos(130*math.pi/180),
        start_lon+r*math.cos(140*math.pi/180),
        start_lon+r*math.cos(5*math.pi/6),
        start_lon+r*math.cos(160*math.pi/180),
        start_lon+r*math.cos(170*math.pi/180),
        start_lon+r*math.cos(math.pi),
        start_lon+r*math.cos(190*math.pi/180),
        start_lon+r*math.cos(200*math.pi/180),
        start_lon+r*math.cos(7*math.pi/6),
        start_lon+r*math.cos(220*math.pi/180),
        start_lon+r*math.cos(230*math.pi/180),
        start_lon+r*math.cos(4*math.pi/3),
        start_lon+r*math.cos(250*math.pi/180),
        start_lon+r*math.cos(260*math.pi/180),
        start_lon+r*math.cos(3*math.pi/2),
        start_lon+r*math.cos(280*math.pi/180),
        start_lon+r*math.cos(290*math.pi/180),
        start_lon+r*math.cos(5*math.pi/3),
        start_lon+r*math.cos(310*math.pi/180),
        start_lon+r*math.cos(320*math.pi/180),
        start_lon+r*math.cos(11*math.pi/6),
        start_lon+r*math.cos(340*math.pi/180),
        start_lon+r*math.cos(350*math.pi/180),
        start_lon+r*math.cos(2*math.pi)]

        lat_list = [start_lat+r*math.sin(10*math.pi/180),
        start_lat+r*math.sin(20*math.pi/180),
        start_lat+r*math.sin(math.pi/6),
        start_lat+r*math.sin(40*math.pi/180),
        start_lat+r*math.sin(50*math.pi/180),
        start_lat+r*math.sin(math.pi/3),
        start_lat+r*math.sin(70*math.pi/180),
        start_lat+r*math.sin(80*math.pi/180),
        start_lat+r*math.sin(math.pi/2),
        start_lat+r*math.sin(100*math.pi/180),
        start_lat+r*math.sin(110*math.pi/180),
        start_lat+r*math.sin(2*math.pi/3),
        start_lat+r*math.sin(130*math.pi/180),
        start_lat+r*math.sin(140*math.pi/180),
        start_lat+r*math.sin(5*math.pi/6),
        start_lat+r*math.sin(160*math.pi/180),
        start_lat+r*math.sin(170*math.pi/180),
        start_lat+r*math.sin(math.pi),
        start_lat+r*math.sin(190*math.pi/180),
        start_lat+r*math.sin(200*math.pi/180),
        start_lat+r*math.sin(7*math.pi/6),
        start_lat+r*math.sin(220*math.pi/180),
        start_lat+r*math.sin(230*math.pi/180),
        start_lat+r*math.sin(4*math.pi/3),
        start_lat+r*math.sin(250*math.pi/180),
        start_lat+r*math.sin(260*math.pi/180),
        start_lat+r*math.sin(3*math.pi/2),
        start_lat+r*math.sin(280*math.pi/180),
        start_lat+r*math.sin(290*math.pi/180),
        start_lat+r*math.sin(5*math.pi/3),
        start_lat+r*math.sin(310*math.pi/180),
        start_lat+r*math.sin(320*math.pi/180),
        start_lat+r*math.sin(11*math.pi/6),
        start_lat+r*math.sin(340*math.pi/180),
        start_lat+r*math.sin(350*math.pi/180),
        start_lat+r*math.sin(2*math.pi)]

        test_df = pd.DataFrame({'lat':lat_list, 'lon':lon_list})
        df = pd.concat([df, test_df])
    return df