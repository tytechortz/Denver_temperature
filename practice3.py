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

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config['suppress_callback_exceptions']=True

# cnx = sqlite3.connect('denvertemps.db')

pd.options.mode.chained_assignment = None  # default='warn'

# df = pd.read_sql_query("SELECT * FROM temperatures", cnx)
df = pd.read_csv('./stapleton.csv')

# daily normal temperatures
df_norms = pd.read_csv('./daily_normal_max.csv')

df['datetime']= pd.to_datetime(df['DATE'])
df = df.set_index('datetime')
df_ya_max = df.resample('Y').mean()
# removes final year in df
df5 = df_ya_max[:-1]

year = []
for YEAR in df.index.year.unique():
    year.append({'label':(YEAR), 'value':YEAR})


body = dbc.Container([
    dbc.Row(
        [
            dbc.Col(
                html.H1('DENVER TEMPERATURE RECORD', style={'text-align':'center', 'font-size':50,'font-color':'Gray'})
            )
        ],
        justify='center'
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
                html.Div(
                    html.H3('DAILY TEMPERATURES'),
                style={'text-align':'center'}
                ),
            ),
        ],
         justify='around',
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='graph1', style={'height':700}),
                ]),
                width={'size':12}
            ),
        ],
        justify='around',
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2('SELECT YEARS', style={'text-align':'center'})
            ),
            dbc.Col(
                html.H2('SELECT PARAMETER', style={'text-align':'center'})
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(id='year-picker', options=year
                ),
                width = {'size': 2}),
            dbc.Col(
                dcc.RadioItems(id='param', options=[
                    {'label':'MAX TEMP','value':'max'},
                    {'label':'MIN TEMP','value':'min'}
                    ],
                ),
                width = {'size': 2}),    
        ],
        justify='around',
    ),
])

@app.callback(Output('graph1', 'figure'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_figure(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    traces = []
    print(param)
    if param == 'max':
        year_param = filtered_year['TMAX']
    else:
        year_param = filtered_year['TMIN']
    # year_MAXT = filtered_year['TMAX']
    # year_MINT = filtered_year["TMIN"]

    traces.append(go.Scatter(
        y = year_param,
        name = param
    ))
    traces.append(go.Scatter(
        y = df_norms['DLY-TMAX-NORMAL'],
        name = "Normal Max T"
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'title': 'DAY'},
            yaxis = {'title': 'TMAX'},
            hovermode = 'closest',
            title = '3 Day Rolling Avg'
        )
    }


app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)