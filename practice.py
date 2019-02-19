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

years = []
for YEAR in df.index.year.unique():
    years.append({'label':(YEAR), 'value':YEAR})

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
                html.Div(
                    html.H3('MAX DAILY TEMP'),
                style={'width':1000, 'text-align':'center'}
                ),
                width = {'size':5,'offset':1},
            ),
            dbc.Col(
                html.Div(
                    html.H3('MIN DAILY TEMP'),
                style={'width':1000, 'text-align':'center'}
                ),
                width = {'size':5}, 
            ),
        ],
         align='center',
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='graph1', style={'height':700, 'width':'1000', 'display':'inline-block'}),
                ]),
                width = {'size': 5, 'offset': 1},
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='graph2', style={'height':700, 'width':'1000', 'display':'inline-block'}),
                ]),
                width = {'size': 5},
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2('SELECT YEARS', style={'text-align':'center'})
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                dcc.Dropdown(id='year-picker1', options=years
                ),
                width = {'size': 3, 'offset': 2}),
            dbc.Col(
                dcc.Dropdown(id='year-picker2', options=years
                ),
                width = {'size': 3, 'offset': 2}),    
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='stats-for-year1',style={'color': 'blue', 'text-align': 'center'},
                ),
                width = {'size': 5, 'offset': 1}),
            dbc.Col(
                html.H2(id='stats-for-year2',style={'color': 'darkorange', 'text-align': 'center'},
                ),
                width = {'size': 5}),
        ],
        align = 'end'
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='Maximum-yearly-temp-1', style={'font-size':25, 'color': 'blue'},
                ),
                width = {'offset': 1, 'size': 3}),
            dbc.Col(
                html.H2(id='Minimum-yearly-temp-1', style={'font-size':25, 'color': 'blue'}
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H2(id='Maximum-yearly-temp-2', style={'font-size':25, 'color': 'darkorange'}
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H2(id='Minimum-yearly-temp-2', style={'font-size':25, 'color': 'orange'}
                ),
                width = {'offset': 1}),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='90-degree-days-1', style={'font-size':25, 'color': 'blue'},
                ),
                width = {'offset': 1, 'size': 3}),
            dbc.Col(
                html.H2(id='High-below-freezing-1', style={'font-size':25, 'color': 'blue'},
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H2(id='90-degree-days-2', style={'font-size':25, 'color': 'darkorange'},
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H2(id='High-below-freezing-2', style={'font-size':25, 'color': 'orange'}
                ),
                width = {'offset': 1}),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='80-degree-days-1', style={'font-size':25, 'color': 'blue'},
                ),
                width = {'offset': 1, 'size': 3}),
            dbc.Col(
                html.H2(id='Low-below-zero-1', style={'font-size':25, 'color': 'blue'},
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H2(id='80-degree-days-2', style={'font-size':25, 'color': 'orange'},
                ),
                width = {'size': 2}),
            dbc.Col(
                html.H2(id='Low-below-zero-2', style={'font-size':25, 'color': 'orange'}
                ),
                width = {'offset': 1}),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='combined-histogram-max', style={'height':700, 'width':1000, 'display':'inline-block'}),
                ]),
                width = {'size':5 ,'offset':1},
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='combined-histogram-min', style={'height':700, 'width':1000, 'display':'inline-block'}),
                ]),
                width = {'size': 5},
            )
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H3(id='stats-for-year1-1',style={'text-align': 'center'},
                ),
                width = {'size': 5, 'offset': 1}),
            dbc.Col(
                html.H3(id='stats-for-year2-2',style={'text-align': 'center'},
                ),
                width = {'size': 5}),
        ],
        align = 'end'
    ),
    # dbc.Row(
    #     [
    #         dbc.Col(
    #             html.Div(
    #                 html.H3('DENVER MAX TEMPS'),
    #             style={'height':100, 'background-color':'lightsilver', 'width':1000, 'text-align': 'center'}
    #             ),
    #             width = {'size':5,'offset':1},
    #         ),
    #         dbc.Col(
    #             html.Div(
    #                 html.H3('DENVER MIN TEMPS, 1948-PRESENT'),
    #             style={'height':100, 'background-color':'lightsilver', 'width':1000, 'text-align': 'center'}
    #             ),
    #             width = {'size':5}, 
    #         ),
    #     ],
    #      align='center',
    # ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='yearly-avg-max-trend', style={'height':700, 'width':1000, 'display':'inline-block'}   ,
                        figure = {
                            'data': [
                                {
                                    'x' : df5.index, 
                                    'y' : df5['TMAX'],
                                    'mode' : 'lines + markers',
                                    'name' : 'Max Temp'
                                },
                                {
                                    'x' : df5.index,
                                    'y' : annual_max_fit(),
                                    'name' : 'trend'
                                }
                            ],
                            'layout': go.Layout(
                                xaxis = {'title': 'Date'},
                                yaxis = {'title': 'Temp'},
                                hovermode = 'closest',
                                height = 1000     
                            ), 
                        }
                    ),

                ]),
                width = {'size': 5, 'offset':1},
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='yearly-avg-min-trend', style={'height':700, 'width':1000, 'display':'inline-block'}   ,
                        figure = {
                            'data': [
                                {
                                    'x' : df5.index, 
                                    'y' : df5['TMIN'],
                                    'mode' : 'lines + markers',
                                    'name' : 'Min Temp'
                                },
                                {
                                    'x' : df5.index,
                                    'y' : annual_min_fit(),
                                    'name' : 'trend'
                                }
                            ],
                            'layout': go.Layout(
                                xaxis = {'title': 'Date'},
                                yaxis = {'title': 'Temp'},
                                hovermode = 'closest',
                                height = 1000     
                            ), 
                        }
                    ),

                ]),
                width = {'size':5},
            ),
        ]
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    html.H3('DENVER MAX TEMPS, 1948-PRESENT'),
                style={'height':100, 'background-color':'lightsilver', 'width':1000, 'text-align': 'center'}
                ),
                width = {'size':5,'offset':1},
            ),
            dbc.Col(
                html.Div(
                    html.H3('DENVER MIN TEMPS, 1948-PRESENT'),
                style={'height':100, 'background-color':'lightsilver', 'width':1000, 'text-align': 'center'}
                ),
                width = {'size':5}, 
            ),
        ],
         align='center',
    ),
    dbc.Row(
        dbc.Col(
            html.Div(id='divider', style={'height':200, 'background-color':'silver'})    
                ),
    ),    
])

@app.callback(Output('graph1', 'figure'),
              [Input('year-picker1', 'value'),
               Input('year-picker2', 'value')])
def update_figure(selected_year1, selected_year2):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df2 = df[df.index.year == selected_year2]
    traces = []
    max_rolling = filtered_df1['TMAX'].rolling(window=3)
    min_rolling = filtered_df2['TMAX'].rolling(window=3)
    rolling_max = max_rolling.mean()
    rolling_min = min_rolling.mean()

    traces.append(go.Scatter(
        y = rolling_max,
        name = selected_year1
    ))
    traces.append(go.Scatter(
        y = rolling_min,
        name = selected_year2
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'title': 'YEAR'},
            yaxis = {'title': 'TMAX'},
            hovermode = 'closest'
        )
    }

@app.callback(Output('graph2', 'figure'),
              [Input('year-picker1', 'value'),
               Input('year-picker2', 'value')])
def update_figure(selected_year1, selected_year2):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df2 = df[df.index.year == selected_year2]
    traces = []
    max_rolling = filtered_df1['TMIN'].rolling(window=3)
    min_rolling = filtered_df2['TMIN'].rolling(window=3)
    rolling_max = max_rolling.mean()
    rolling_min = min_rolling.mean()

    traces.append(go.Scatter(
        y = rolling_max,
        name = selected_year1
    ))
    traces.append(go.Scatter(
        y = rolling_min,
        name = selected_year2
    ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis = {'title': 'YEAR'},
            yaxis = {'title': 'TMAX'},
            hovermode = 'closest'
        )
    } 

@app.callback(Output('stats-for-year1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_i(selected_year1):
    return 'Stats for {}'.format(selected_year1)

@app.callback(Output('stats-for-year2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_j(selected_year2):
    return 'Stats for {}'.format(selected_year2)

@app.callback(Output('Maximum-yearly-temp-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_a(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    annual_max_temp1 = filtered_df1['TMAX'].max()
    return 'Maximum Yearly Temp: {:.0f}'.format(annual_max_temp1)

@app.callback(Output('Minimum-yearly-temp-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_b(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    annual_min_temp1 = filtered_df1['TMIN'].min()
    return 'Minimum Yearly Temp: {:.0f}'.format(annual_min_temp1)

@app.callback(Output('Maximum-yearly-temp-2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_c(selected_year2):
    filtered_df1 = df[df.index.year == selected_year2]
    annual_max_temp2 = filtered_df1['TMAX'].max()
    return 'Maximum Yearly Temp: {:.0f}'.format(annual_max_temp2)

@app.callback(Output('Minimum-yearly-temp-2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_d(selected_year2):
    filtered_df1 = df[df.index.year == selected_year2]
    annual_min_temp2 = filtered_df1['TMIN'].min()
    return 'Minimum Yearly Temp: {:.0f}'.format(annual_min_temp2)

@app.callback(Output('90-degree-days-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_e(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').max()
    days_over_90 = (df_max[df_max['TMAX'] >= 90].count()['TMAX'])
    return 'Total Days Above 90 : {}'.format(days_over_90)

@app.callback(Output('High-below-freezing-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_f(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').max()
    days_high_below_zero = (df_max[df_max['TMAX'] < 32].count()['TMAX'])
    return 'Days High Below Freezing : {:.0f}'.format(days_high_below_zero)

@app.callback(Output('90-degree-days-2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_g(selected_year2):
    filtered_df1 = df[df.index.year == selected_year2]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').max()
    days_over_90 = (df_max[df_max['TMAX'] >= 90].count()['TMAX'])
    return 'Total Days Above 90 : {}'.format(days_over_90)

@app.callback(Output('High-below-freezing-2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_h(selected_year2):
    filtered_df1 = df[df.index.year == selected_year2]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').max()
    days_high_below_zero = (df_max[df_max['TMAX'] < 32].count()['TMAX'])
    return 'Days High Below Freezing : {:.0f}'.format(days_high_below_zero)

@app.callback(Output('80-degree-days-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_m(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').max()
    days_over_80 = (df_max[df_max['TMAX'] >= 80].count()['TMAX'])
    return 'Total Days Above 80 : {}'.format(days_over_80)

@app.callback(Output('Low-below-zero-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_n(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').min()
    days_low_below_zero = (df_max[df_max['TMIN'] < 0].count()['TMIN'])
    return 'Days Low Below 0 : {:.0f}'.format(days_low_below_zero)


@app.callback(Output('80-degree-days-2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_k(selected_year2):
    filtered_df1 = df[df.index.year == selected_year2]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').max()
    days_over_80 = (df_max[df_max['TMAX'] >= 80].count()['TMAX'])
    return 'Total Days Above 80 : {}'.format(days_over_80)

@app.callback(Output('Low-below-zero-2', 'children'),
              [Input('year-picker2', 'value')])
def update_layout_l(selected_year2):
    filtered_df1 = df[df.index.year == selected_year2]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    df_max = filtered_df1.resample('D').min()
    days_low_below_zero = (df_max[df_max['TMIN'] < 0].count()['TMIN'])
    return 'Days Low Below 0 : {:.0f}'.format(days_low_below_zero)

@app.callback(Output('combined-histogram-max','figure'),
              [Input('year-picker1', 'value'),
              Input('year-picker2', 'value')])

def update_graph_a(selected_year1,selected_year2):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    filtered_df2 = df[df.index.year == selected_year2]
    filtered_df2['datetime'] = pd.to_datetime(filtered_df2['DATE'])
    filtered_df2 = filtered_df2.set_index('datetime')
    
    trace1 = go.Histogram(
        x=filtered_df1['TMAX'],
        opacity=.5,
        xbins=dict(size=10),
        name = selected_year1
    )

    trace2 = go.Histogram(
        x=filtered_df2['TMAX'],
        opacity=.5,
        xbins=dict(size=10),
        name = selected_year2
    )

    data = [trace1, trace2]

    fig = go.Figure(
        data = data,
        layout = go.Layout(barmode='overlay')
        )
    return fig


# Histogram of minimum daily temps for two selected years
@app.callback(Output('combined-histogram-min','figure'),
              [Input('year-picker1', 'value'),
              Input('year-picker2', 'value')])

def update_graph_b(selected_year1,selected_year2):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
    filtered_df1 = filtered_df1.set_index('datetime')
    filtered_df2 = df[df.index.year == selected_year2]
    filtered_df2['datetime'] = pd.to_datetime(filtered_df2['DATE'])
    filtered_df2 = filtered_df2.set_index('datetime')
    
    trace1 = go.Histogram(
        x = filtered_df1['TMIN'],
        opacity = .5,
        xbins = dict(size = 10),
        name = selected_year1
    )

    trace2 = go.Histogram(
        x = filtered_df2['TMIN'],
        opacity = .5,
        xbins = dict(size=10),
        name = selected_year2
    )

    data = [trace1, trace2]

    fig = go.Figure(
        data = data,
        layout = go.Layout(barmode='overlay')
        )
    return fig

@app.callback(Output('stats-for-year1-1', 'children'),
              [Input('year-picker1', 'value'),
              Input('year-picker2', 'value')])
def update_layout_o(selected_year1, selected_year2):
    return 'Max Temps: {} and {}'.format(selected_year1,selected_year2)

@app.callback(Output('stats-for-year2-2', 'children'),
              [Input('year-picker2', 'value'),
              Input('year-picker1', 'value')])
def update_layout_p(selected_year2, selected_year1):
    return 'Min Temps: {} and {}'.format(selected_year1,selected_year2)

if __name__ == "__main__":
    app.run_server(port=8124, debug=True)