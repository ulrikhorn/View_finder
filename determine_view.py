import urllib3
import re
import pandas as pd
import math
import numpy as np
from circular_locations import straightlines
import time


df = pd.read_csv("coord_elevation_df2.csv")
itt = list(np.arange(0,36,1))*int(len(df)/36)
df = df.assign(iteration = itt)
print(df)