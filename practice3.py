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
df_norms_max = pd.read_csv('./daily_normal_max.csv')
df_norms_min = pd.read_csv('./daily_normal_min.csv')

df['datetime']= pd.to_datetime(df['DATE'])
df = df.set_index('datetime')

# record high and low
record_max = df.loc[df['TMAX'].idxmax()]
record_min = df.loc[df['TMIN'].idxmin()]

df_ya_max = df.resample('Y').mean()
# removes final year in df
df5 = df_ya_max[:-1]

# sorts annual mean temps
annual_max_mean_rankings = df5['TMAX'].sort_values(axis=0, ascending=True)
annual_min_mean_rankings = df5['TMIN'].sort_values(axis=0, ascending=True)
drl = annual_max_mean_rankings.size

# current year stats
current_year = datetime.now().year
current_day = datetime.now().day
df_cy = df.loc['2019-01-01':]



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
                html.H2('SELECT YEAR', style={'text-align':'center'})
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
    dbc.Row([
            dbc.Col(
                html.Div(
                    html.H3(id='stats',style={'text-align':'center'}),
                ),
            ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Yearly High: {:,.1f} Deg F, {}".format(record_max['TMAX'], record_max['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("Yearly Low: {:,.1f} Deg F, {}".format(record_min['TMIN'], record_min['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Record High: {:,.1f} Deg F, {}".format(record_max['TMAX'], record_max['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("Record Low: {:,.1f} Deg F, {}".format(record_min['TMIN'], record_min['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4('Warmest Years-Mean Max ',style={'color': 'black','font-size':20}),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Warmest Years-Mean Min',style={'color': 'black','font-size':20}),
                ]),
                width={'size':6},
                style={'height':30, 'text-align':'center'} 
            ),
        ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("1- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-1], annual_max_mean_rankings.index[drl-1].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-1], annual_min_mean_rankings.index[drl-1].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-2], annual_max_mean_rankings.index[drl-2].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-2], annual_min_mean_rankings.index[drl-2].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("3- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-3], annual_max_mean_rankings.index[drl-3].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-3], annual_min_mean_rankings.index[drl-3].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("4- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-4], annual_max_mean_rankings.index[drl-4].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-4], annual_min_mean_rankings.index[drl-4].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("5- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-5], annual_max_mean_rankings.index[drl-5].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-5], annual_min_mean_rankings.index[drl-5].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("6- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-6], annual_max_mean_rankings.index[drl-6].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-6], annual_min_mean_rankings.index[drl-6].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("7- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-7], annual_max_mean_rankings.index[drl-7].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-7], annual_min_mean_rankings.index[drl-7].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("8- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-8], annual_max_mean_rankings.index[drl-8].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-8], annual_min_mean_rankings.index[drl-8].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("9- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-9], annual_max_mean_rankings.index[drl-9].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-9], annual_min_mean_rankings.index[drl-9].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("10- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-10], annual_max_mean_rankings.index[drl-10].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-10], annual_min_mean_rankings.index[drl-10].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    
])

@app.callback(Output('graph1', 'figure'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_figure(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    traces = []
    year_param_max = filtered_year['TMAX']
    year_param_min = filtered_year['TMIN']
    print(param)
    if param == 'max':
        traces.append(go.Scatter(
        y = year_param_max,
        name = param
        ))
        traces.append(go.Scatter(
            y = df_norms_max['DLY-TMAX-NORMAL'],
            name = "Normal Max T"
        ))
    elif param == 'min':  
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
            title = '3 Day Rolling Avg'
        )
    }

@app.callback(Output('stats', 'children'),
              [Input('year-picker', 'value')])
def update_layout_i(selected_year1):
    return 'Stats for {}'.format(selected_year1)


app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)