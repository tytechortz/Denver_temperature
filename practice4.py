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

df['date'] = pd.to_datetime(df['DATE'])
df = df.set_index('date')

df_ya_max = df.resample('Y').mean()

df.loc[:,'TAVG'] = ((df.TMAX + df.TMIN) / 2)

# record high and low
record_max = df.loc[df['TMAX'].idxmax()]
record_min = df.loc[df['TMIN'].idxmin()]

df_ya_max = df.resample('Y').mean()
df_da = df_ya_max.groupby((df_ya_max.index.year//10)*10).mean()


# removes final year in df
df5 = df_ya_max[:-1]
# removes final decade in decade averages
df10 = df_da[0:-1]

# filters for completed years in current decade
current_year_decade = current_year%10
current_year_indexer = current_year_decade + 1
# current year decade avg current decade
df_da_cd = (df5[-(current_year_indexer):]).mean()
# current year 90- degree days
cy90 = df_new[df_new['TMAX']>=90]

# add current decade to decade list
df10.loc['2010'] = df_da_cd
df10 = df10.round(1)
df10 = df10.reset_index()

# current year stats
cy_max = df_new.loc[df_new['TMAX'].idxmax()]
cy_min = df_new.loc[df_new['TMIN'].idxmin()]
cy_max_mean = df_new['TMAX'].mean()
cy_min_mean = df_new['TMIN'].mean()

# filters all MAXT data for 5 year moving average
allmax_rolling = df['TMAX'].rolling(window=1825)
allmax_rolling_mean = allmax_rolling.mean()
# filters all MINT data fr 5 year moving average
allmin_rolling = df['TMIN'].rolling(window=1825)
allmin_rolling_mean = allmin_rolling.mean()

startyr = 1950
presentyr = datetime.now().year
year_count = presentyr-startyr

# linear fit for Avg Max Temps
def annual_min_fit():
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMIN"])
    return (slope*xi+intercept)

def annual_max_fit():
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMAX"])
    return (slope*xi+intercept)

def all_max_temp_fit():
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMAX"])
    return (slope*xi+intercept)

def all_min_temp_fit():
    xi = arange(0,year_count)
    slope, intercept, r_value, p_value, std_err = stats.linregress(xi,df5["TMIN"])
    return (slope*xi+intercept)

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
                dcc.Graph(id='graph1', style={'height':600}),
            ]),
            width={'size':10}
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
            dbc.Col(
                html.Div(
                    html.H3(id='stats',style={'text-align':'center'}),
                ),
            ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(id='yearly-high/low')
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H5(id='mean-max/min'),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(id='days-above-100/below-0')
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H5(id='days-above-90/high-below-0'),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H5(id='days-above-80/below-32')
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H5(id='days-above-normal/below-normal'),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.H2('STUFF', style={'text-align':'center'})
        )]
    ),
    dbc.Row([
        dbc.Col(
            dcc.RadioItems(id='selection', options=[
                {'label':'Decade Rankings','value':'decades'},
                {'label':'100 Degree Days','value':'100-degrees'},
                {'label':'90 Degree Days','value':'90-degrees'},
                ]),
            width = {'size': 4}), 
    ],
    justify='around',
    ),
    dbc.Row([
        dbc.Col(
            dash_table.DataTable(
                id='temptable',
                columns=[{}],
                data=[{}],
                sorting=True,
                style_cell={'textAlign': 'center'},
                style_as_list_view=True,
                style_table={
                    'maxHeight': '450',
                    'overflowY': 'scroll'
                },
            ),
        ),
        dbc.Col(
            dcc.Graph(id='bar'),
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.H2('STUFF', style={'text-align':'center'})
        )]
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
    dbc.Row([
        dbc.Col(
            html.H2('STUFF', style={'text-align':'center'})
        )]
    ),
    dbc.Row(
        [
           dbc.Col(
                html.Div([
                    dcc.Graph(id='all-max-temps',  
                        figure = {
                            'data': [
                                {
                                    'x' : df.index, 
                                    'y' : allmax_rolling_mean,
                                    'mode' : 'lines + markers',
                                    'name' : 'Max Temp'
                                },
                                {
                                    'x' : df5.index,
                                    'y' : all_max_temp_fit(),
                                    'name' : 'trend'
                                }
                            ],
                            'layout': go.Layout(
                                xaxis = {'title': 'Date'},
                                yaxis = {'title': 'Temp'},
                                hovermode = 'closest',
                                height = 700     
                            ), 
                        }
                    ),
                ]),
                width = {'size': 10, 'offset':1},
            ), 
        ],
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H3('Max Temps 1950-Present, 5 Year Moving Avg', style={'height':50, 'text-align': 'center'}),
                ),
        ],
        align = 'around'
    ),
    dbc.Row(
        [
           dbc.Col(
                html.Div([
                    dcc.Graph(id='all-min-temps',  
                        figure = {
                            'data': [
                                {
                                    'x' : df.index, 
                                    'y' : allmin_rolling_mean,
                                    'mode' : 'lines + markers',
                                    'name' : 'Max Temp'
                                },
                                {
                                    'x' : df5.index,
                                    'y' : all_min_temp_fit(),
                                    'name' : 'trend'
                                }
                            ],
                            'layout': go.Layout(
                                xaxis = {'title': 'Date'},
                                yaxis = {'title': 'Temp'},
                                hovermode = 'closest',
                                height = 700     
                            ), 
                        }
                    ),

                ]),
                width = {'size': 10, 'offset':1},
            ), 
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H3('Min Temps 1950-Present, 5 Year Moving Avg', style={'height':50, 'text-align': 'center'}),
                ),
        ],
        align = 'around'
    ),
])

@app.callback(Output('graph1', 'figure'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_figure(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    traces = []
    year_param_max = filtered_year['' + param + '']
    year_param_min = filtered_year[''+ param + '']
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

@app.callback(Output('yearly-high/low', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_b(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    yearly_max = filtered_year.loc[filtered_year['' + param + ''].idxmax()]
    yearly_min = filtered_year.loc[filtered_year['' + param + ''].idxmin()]
    print(yearly_max)
    if param == 'TMAX':
        return 'Yearly High: {}, {}'.format(yearly_max['TMAX'], yearly_max['DATE'])
    elif param == 'TMIN':
        return 'Yearly Low: {}, {}'.format(yearly_min['TMIN'], yearly_min['DATE'])

@app.callback(Output('mean-max/min', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_c(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    if param == 'TMAX':
        return 'Mean Max Temp: {:,.1f}'.format(filtered_year['TMAX'].mean())
    elif param == 'TMIN':
        return 'Mean Min Temp: {:,.1f}'.format(filtered_year['TMIN'].mean())

@app.callback(Output('days-above-100/below-0', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_d(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    da_hundred = (filtered_year['TMAX'] >= 100).sum()
    da_below_zero = (filtered_year['TMIN'] < 0).sum()
    if param == 'TMAX':
        return '100 Degree Days: {} - Normal: 8'.format(da_hundred)
    elif param == 'TMIN':
        return 'Days Below 0: {} - Normal: 6.7'.format(da_below_zero)

@app.callback(Output('days-above-90/high-below-0', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_e(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    da_ninety = (filtered_year['TMAX'] >= 90).sum()
    da_high_below_32 = (filtered_year['TMAX'] < 32).sum()
    if param == 'TMAX':
        return '90 Degree Days: {} - Normal: 30.6'.format(da_ninety)
    elif param == 'TMIN':
        return 'Days High Below 32: {} - Normal: 21'.format(da_high_below_32)

@app.callback(Output('days-above-80/below-32', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_f(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    da_80 = (filtered_year['TMAX'] >= 80).sum()
    da_below_32 = (filtered_year['TMIN'] < 32).sum()
    if param == 'TMAX':
        return '80 Degree Days: {} - Normal: 95.5'.format(da_80)
    elif param == 'TMIN':
        return 'Days Below 0: {} - Normal: 156.5'.format(da_below_32)

@app.callback(Output('days-above-normal/below-normal', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_g(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    dmaxan = 0
    dminan = 0
    i = 0
    df_norms_max.loc[i]['DLY-TMAX-NORMAL'] 
    if param == 'TMAX':
        while i < filtered_year["TMAX"].count():
            if filtered_year.iloc[i]['TMAX'] > df_norms_max.iloc[i]['DLY-TMAX-NORMAL']:
                dmaxan = dmaxan + 1
                i = i + 1
            else: i = i + 1    
        return 'Days High Above Normal: {}/{}'.format(dmaxan, i)
    elif param == 'TMIN':
        while i < filtered_year["TMIN"].count():
            if filtered_year.iloc[i]['TMIN'] < df_norms_min.iloc[i]['DLY-TMIN-NORMAL']:
                dminan = dminan + 1
                i = i + 1
            else: i = i + 1
        return 'Days Low Below Normal: {}/{}'.format(dminan, i)

@app.callback(Output('temptable', 'columns'),
             [Input('selection', 'value')])
def update_table_a(selection):
    df_100 = df[df['TMAX']>=100]
    df_100_count = df_100.resample('Y').count()['TMAX']
    df_100 = pd.DataFrame({'date':df_100_count.index, '100 Degree Days':df_100_count.values})
    df_90 = df[df['TMAX']>=90]
    df_90_count = df_90.resample('Y').count()['TMAX']
    df_90 = pd.DataFrame({'date':df_90_count.index, '90 Degree Days':df_90_count.values})
    if selection == 'decades':
        return [{'name': i, 'id': i} for i in df10.columns]
    elif selection == '100-degrees':
        return [{'name': i, 'id': i} for i in df_100.columns]
    elif selection == '90-degrees':
        return [{'name': i, 'id': i} for i in df_90.columns]
        
@app.callback(Output('temptable', 'data'),
             [Input('selection', 'value')])
def create_table_b(selection):
    df_100 = df[df['TMAX']>=100]
    df_100_count = df_100.resample('Y').count()['TMAX']
    df_100 = pd.DataFrame({'date':df_100_count.index, '100 Degree Days':df_100_count.values})
    df_90 = df[df['TMAX']>=90]
    df_90_count = df_90.resample('Y').count()['TMAX']
    df_90 = pd.DataFrame({'date':df_90_count.index, '90 Degree Days':df_90_count.values})
    if selection == 'decades':
        return df10.to_dict('records')
    elif selection == '100-degrees':
        return df_100.to_dict('records')
    elif selection == '90-degrees':
        return df_90.to_dict('records')

@app.callback(Output('bar', 'figure'),
             [Input('selection', 'value')])
def update_figure_a(selection):
    df_100 = df[df['TMAX']>=100]
    df_100_count = df_100.resample('Y').count()['TMAX']
    df_100 = pd.DataFrame({'date':df_100_count.index, '100 Degree Days':df_100_count.values})
    df_90 = df[df['TMAX']>=90]
    df_90_count = df_90.resample('Y').count()['TMAX']
    df_90 = pd.DataFrame({'date':df_90_count.index, '90 Degree Days':df_90_count.values})
    if selection == 'decades':
        data = [
            go.Bar(
                x=df10['date'],
                y=df10['TAVG']
            )
        ]
        layout = go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': 'TAVG'},
            title='Avg Temp by Decade'
        )
        return {'data': data, 'layout': layout} 
    elif selection == '100-degrees':
        data = [
            go.Bar(
                x=df_100['date'],
                y=df_100['100 Degree Days']
            )
        ]
        layout = go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': '100 Degree Days'},
            title='100 Degree Days Per Year'
        ) 
        return {'data': data, 'layout': layout}
    elif selection == '90-degrees':
        data = [
            go.Bar(
                x=df_90['date'],
                y=df_90['90 Degree Days']
            )
        ]
        layout = go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': '90 Degree Days'},
            title='90 Degree Days Per Year'
        ) 
        return {'data': data, 'layout': layout}



app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)