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
from scipy.stats import norm 
from numpy import arange,array,ones 
import dash_table

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

current_year = datetime.now().year
current_day = datetime.now().day
today = time.strftime("%Y-%m-%d")

# daily normal temperatures
df_norms_max = pd.read_csv('./daily_normal_max.csv')
df_norms_min = pd.read_csv('./daily_normal_min.csv')

# daily normal temperatures
df_norms_max = pd.read_csv('./daily_normal_max.csv')
df_norms_min = pd.read_csv('./daily_normal_min.csv')

df_old = pd.read_csv('./stapleton.csv').round(1)
df_new = pd.read_csv('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN&stations=USW00023062&startDate=2019-01-01&endDate=' + today + '&units=standard').round(1)
df = pd.concat([df_old, df_new], ignore_index=True)

df['datetime'] = pd.to_datetime(df['DATE'])
df = df.set_index('datetime')
print(df)

# year list for dropdown selector
year = []
for YEAR in df.index.year.unique():
    year.append({'label':(YEAR), 'value':YEAR})



body = dbc.Container([

])


@app.callback(Output('stats', 'children'),
              [Input('year-picker', 'value')])
def update_layout_a(selected_year):
    return 'Stats for {}'.format(selected_year)


    



app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)