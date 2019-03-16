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

df['DATE'] = pd.to_datetime(df['DATE'])
df = df.set_index('DATE')

df_ya_max = df.resample('Y').mean()

df.loc[:,'TAVG'] = ((df.TMAX + df.TMIN) / 2)

# record high and low
record_max = df.loc[df['TMAX'].idxmax()]
record_min = df.loc[df['TMIN'].idxmin()]

df_ya_max = df.resample('Y').mean()
df_da = df_ya_max.groupby((df_ya_max.index.year//10)*10).mean()

# removes final year in df
df5 = df_ya_max[:-1]
# removes final decade in dacade averages
df10 = df_da[0:-1]

# filters for completed years in current decade
current_year_decade = current_year%10
current_year_indexer = current_year_decade + 1
# current year decade avg current decade
df_da_cd = (df5[-(current_year_indexer):]).mean()
# add current decade to decade list
df10.loc['2010'] = df_da_cd
df10 = df10.round(1)
df10 = df10.reset_index()

# year list for dropdown selector
year = []
for YEAR in df.index.year.unique():
    year.append({'label':(YEAR), 'value':YEAR})

body = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1('DENVER TEMPERATURE RECORD', style={'text-align':'center', 'font-size':50,'font-color':'Gray'})
        )
    ],
    justify='center'
    ),
    dbc.Row([
        dbc.Col(
            html.H2('1948-PRESENT', style={'text-align':'center'})
        )]
    ),
    dbc.Row([
        dbc.Col(
            html.Div(
                html.H3('DAILY TEMPERATURES'),
            style={'text-align':'center'}
            ),
        )
    ],
    justify='around',
    ),
    dbc.Row([
        dbc.Col(
            html.Div([
                dcc.Graph(id='graph1', style={'height':700}),
            ]),
            width={'size':12}
        ),
    ],
    justify='around',
    ),
    dbc.Row([
        dbc.Col(
            html.H2('SELECT YEAR', style={'text-align':'center'})
        ),
        dbc.Col(
            html.H4('Data Updated', style={'text-align':'center'})
        ),
        dbc.Col(
            html.H2('SELECT PARAMETER', style={'text-align':'center'})
        ),
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Dropdown(id='year-picker', options=year
            ),
            width = {'size': 2}),
        dbc.Col(
            html.H4('{}-{}-{}'.format(df.index[-1].year,df.index[-1].month,df.index[-1].day), style={'text-align': 'center'}),
            width = {'size': 2}),
        dbc.Col(
            dcc.RadioItems(id='param', options=[
                {'label':'MAX TEMP','value':'TMAX'},
                {'label':'MIN TEMP','value':'TMIN'}
                ]),
            width = {'size': 2}),    
    ],
    justify='around',
    ),
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                data=df10.to_dict('rows'),
                columns=[{'id': c, 'name': c} for c in df10.columns]
            ),
        ]),
        dbc.Col([
            html.H3('stuff')
        ])
    ]),
])

@app.callback(Output('graph1', 'figure'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_figure(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    traces = []
    year_param_max = filtered_year['' + param + '']
    year_param_min = filtered_year[''+ param + '']
    print(param)
    if param == 'TMAX':
        traces.append(go.Scatter(
        y = year_param_max,
        name = param
        ))
        traces.append(go.Scatter(
            y = df_norms_max['DLY-TMAX-NORMAL'],
            name = "Normal Max T"
        ))
    elif param == 'TMIN':  
        traces.append(go.Scatter(
        y = year_param_min,
        name = param
        ))
        traces.append(go.Scatter(
            y = df_norms_min['DLY-TMIN-NORMAL'],
            name = "Normal Min T"
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'title': 'DAY'},
            yaxis = {'title': 'TMAX'},
            hovermode = 'closest',
            title = ''
        )
    }

@app.callback(Output('stats', 'children'),
              [Input('year-picker', 'value')])
def update_layout_a(selected_year):
    return 'Stats for {}'.format(selected_year)



app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)