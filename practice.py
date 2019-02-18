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



app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

cnx = sqlite3.connect('denvertemps.db')



# df = pd.read_sql_query("SELECT * FROM temperatures", cnx)
df = pd.read_csv('../../stapleton.csv')


df['datetime']= pd.to_datetime(df['DATE'])
df = df.set_index('datetime')
df_ya_max = df.resample('Y').mean()
# removes final year in df
df5 = df_ya_max[:-1]


# filters all MAXT data for 365 moving average
allmax_rolling = df['TMAX'].rolling(window=365)
allmax_rolling_mean = allmax_rolling.mean()

startyr = 1948
presentyr = datetime.now().year
year_count = presentyr-startyr


xi = arange(0,year_count-1)

# linear fit for Avg Max Temps
def annual_min_fit():
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMIN"])
    return (slope*xi+intercept)

def annual_max_fit():
    xi = arange(0,71)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMAX"])
    return (slope*xi+intercept)

def all_temp_fit():
    xi = arange(0,71)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMAX"])
    return (slope*xi+intercept)

years = []
for YEAR in df.index.year.unique():
    years.append({'label':(YEAR), 'value':YEAR})

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(
                html.H1('DENVER TEMPERATURE RECORD', style={'text-align':'center'})
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2('1948-PRESENT', style={'text-align':'center'})
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    html.H3('Denver Max Daily Temp', style={'text-align': 'center', 'color': 'blue'}),
                ])
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='graph', style={'height':700, 'width':1200, 'display':'inline-block'}),
                ]),
                width = {'size': 8, 'offset': 2},
            )
        ]
    ),
])
    

if __name__ == "__main__":
    app.run_server(port=8124, debug=True)