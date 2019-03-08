import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import time
# import datetime
from datetime import datetime
from pandas import Series
from scipy import stats 
from numpy import arange,array,ones 

url = 'ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/all/USW00023062.dly'
df = pd.read_fwf('./USW00023062.dly', header=None, skiprows = 86 )

filtered_df = df[df[0].str.contains("TM")] 
print(filtered_df)