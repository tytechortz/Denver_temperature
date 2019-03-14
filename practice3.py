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

current_year = datetime.now().year
current_day = datetime.now().day
today = time.strftime("%Y-%m-%d")

# daily normal temperatures
df_norms_max = pd.read_csv('./daily_normal_max.csv')
df_norms_min = pd.read_csv('./daily_normal_min.csv')

# df = pd.read_sql_query("SELECT * FROM temperatures", cnx)
df_old = pd.read_csv('./stapleton.csv')
df_new = pd.read_csv('https://www.ncei.noaa.gov/access/services/data/v1?dataset=daily-summaries&dataTypes=TMAX,TMIN&stations=USW00023062&startDate=2019-01-01&endDate=' + today + '&units=standard')
df = pd.concat([df_old, df_new])


df['datetime'] = pd.to_datetime(df['DATE'])
df = df.set_index('datetime')
# df_new['datetime'] = pd.to_datetime(df_new['DATE'])
# df_new = df_new.set_index('datetime')

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
# current_year_index = current_year[-1]
print(current_year)
current_year_decade = current_year%10
current_year_indexer = current_year_decade + 1
print(current_year_indexer)
df_da_cd = (df5[-(current_year_indexer):]).mean()
df_da_cd['combined'] = (df_da_cd['TMAX'] + df_da_cd['TMIN']) / 2
df5['combined'] = (df5['TMAX'] + df5['TMIN']) / 2
df10['combined'] = (df10['TMAX'] + df10['TMIN']) / 2

df_da['combined'] = (df_da['TMAX'] + df_da['TMIN']) / 2
# add current decade to decade list
df10.loc['2010'] = df_da_cd
print(df10)


# sorts annual mean temps
annual_max_mean_rankings = df5['TMAX'].sort_values(axis=0, ascending=True)
annual_min_mean_rankings = df5['TMIN'].sort_values(axis=0, ascending=True)
annual_combined_rankings = df5['combined'].sort_values(axis=0, ascending=True)
drl = annual_max_mean_rankings.size

# current year stats
cy_max = df_new.loc[df_new['TMAX'].idxmax()]
cy_min = df_new.loc[df_new['TMIN'].idxmin()]
cy_max_mean = df_new['TMAX'].mean()
cy_min_mean = df_new['TMIN'].mean()

# days max above normal
dmaxan = 0
i = 0
while i < df_new['TMAX'].count():
    if df_new.loc[i]['TMAX'] > df_norms_max.loc[i]['DLY-TMAX-NORMAL']:
        dmaxan = dmaxan + 1
        i = i + 1
    else:i = i + 1

# day min above normal
dminan = 0
i = 0
while i < df_new['TMIN'].count():
    if df_new.loc[i]['TMIN'] > df_norms_min.loc[i]['DLY-TMIN-NORMAL']:
        dminan = dminan + 1
        i = i + 1
    else:i = i + 1

# year list for dropdown selector
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
                html.H4('Data Updated', style={'text-align':'center'})
            ),
            dbc.Col(
                html.H2('SELECT PARAMETER', style={'text-align':'center'})
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(id='year-picker', options=year
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H4('{}'.format(df['DATE'][-1]), style={'text-align': 'center'}),
                width = {'size': 2}),
            dbc.Col(
                dcc.RadioItems(id='param', options=[
                    {'label':'MAX TEMP','value':'max'},
                    {'label':'MIN TEMP','value':'min'}
                    ]),
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
                html.H6("Yearly High: {:,.1f} Deg F, {}".format(cy_max['TMAX'], cy_max['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("Yearly Low: {:,.1f} Deg F, {}".format(cy_min['TMIN'], cy_min['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("YTD Mean Max: {:,.1f} Deg F".format(cy_max_mean)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("YTD Mean Min: {:,.1f} Deg F".format(cy_min_mean)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("Days High Above Normal: {} ".format(dmaxan)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("Days Low Above Normal: {} ".format(dminan)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
            dbc.Col(
                html.Div(
                    html.H3('RECORDS',style={'text-align':'center'}),
                ),
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
                html.H6("Most 90 Degree Days: {:,.1f} Deg F, {}".format(record_max['TMAX'], record_max['DATE'])),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("Most Days Below 0: {:,.1f} Deg F, {}".format(record_min['TMIN'], record_min['DATE'])),
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
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Warmest Years-Mean Min',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Warmest Years-Overall',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
        ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("1- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-1], annual_max_mean_rankings.index[drl-1].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-1], annual_min_mean_rankings.index[drl-1].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-1], annual_combined_rankings.index[drl-1].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-2], annual_max_mean_rankings.index[drl-2].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-2], annual_min_mean_rankings.index[drl-2].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-2], annual_combined_rankings.index[drl-2].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("3- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-3], annual_max_mean_rankings.index[drl-3].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-3], annual_min_mean_rankings.index[drl-3].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-3], annual_combined_rankings.index[drl-3].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("4- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-4], annual_max_mean_rankings.index[drl-4].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-4], annual_min_mean_rankings.index[drl-4].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-4], annual_combined_rankings.index[drl-4].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("5- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-5], annual_max_mean_rankings.index[drl-5].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-5], annual_min_mean_rankings.index[drl-5].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-5], annual_combined_rankings.index[drl-5].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("6- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-6], annual_max_mean_rankings.index[drl-6].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-6], annual_min_mean_rankings.index[drl-6].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-6], annual_combined_rankings.index[drl-6].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("7- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-7], annual_max_mean_rankings.index[drl-7].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-7], annual_min_mean_rankings.index[drl-7].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-8], annual_combined_rankings.index[drl-7].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("8- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-8], annual_max_mean_rankings.index[drl-8].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-8], annual_min_mean_rankings.index[drl-8].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-8], annual_combined_rankings.index[drl-8].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("9- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-9], annual_max_mean_rankings.index[drl-9].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-9], annual_min_mean_rankings.index[drl-9].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-9], annual_combined_rankings.index[drl-9].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("10- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-10], annual_max_mean_rankings.index[drl-10].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-10], annual_min_mean_rankings.index[drl-10].year)),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10- {:,.1f} Deg F,  {}".format(annual_combined_rankings[drl-10], annual_combined_rankings.index[drl-10].year)),
            ]),
            width={'size':4},
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
            title = ''
        )
    }

@app.callback(Output('stats', 'children'),
              [Input('year-picker', 'value')])
def update_layout_i(selected_year1):
    return 'Stats for {}'.format(selected_year1)


app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)