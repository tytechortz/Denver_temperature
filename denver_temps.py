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




# filters all MAXT data for 5 year moving average
allmax_rolling = df['TMAX'].rolling(window=1825)
allmax_rolling_mean = allmax_rolling.mean()

# filters all MINT data fr 5 year moving average
allmin_rolling = df['TMIN'].rolling(window=1825)
allmin_rolling_mean = allmin_rolling.mean()

# sorts annual mean temps

annual_max_mean_rankings = df5['TMAX'].sort_values(axis=0, ascending=True)
annual_min_mean_rankings = df5['TMIN'].sort_values(axis=0, ascending=True)
drl = annual_max_mean_rankings.size
print(df5['TMIN'])




startyr = 1948
presentyr = datetime.now().year
year_count = presentyr-startyr


xi = arange(0,year_count-1)

year = []
for YEAR in df.index.year.unique():
    year.append({'label':(YEAR), 'value':YEAR})

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

# year = []
# for YEAR in df.index.year.unique():
#     year.append({'label':(YEAR), 'value':YEAR})

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
                width={'size':10}
            ),
        ],
        justify='around',
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2('SELECT YEARS', style={'text-align':'center'})
            )
        ],
        [
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
                    {'label':'MAX','value':'max'},
                    {'label':'MIN','value':'min'}
                    ],
                ),
                width = {'size': 2}),    
        ],
        justify='around',
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='stats-for-year1',style={'color': 'blue', 'text-align': 'center'}),
                ),
            dbc.Col(
                html.H2(id='stats-for-year2',style={'color': 'darkorange', 'text-align': 'center'}),
                ),       
        ],
        justify='around'
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='Maximum-yearly-temp-1', style={'font-size':25, 'color': 'blue', 'text-align':'center'}),
                width=6, lg=3),     
            dbc.Col(
                html.H2(id='Minimum-yearly-temp-1', style={'font-size':25, 'color': 'blue', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='Maximum-yearly-temp-2', style={'font-size':25, 'color': 'darkorange', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='Minimum-yearly-temp-2', style={'font-size':25, 'color': 'darkorange', 'text-align':'center'}),
                width=6, lg=3),  
        ],
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='90-degree-days-1', style={'font-size':25, 'color': 'blue', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='High-below-freezing-1', style={'font-size':25, 'color': 'blue', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='90-degree-days-2', style={'font-size':25, 'color': 'darkorange', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='High-below-freezing-2', style={'font-size':25, 'color': 'darkorange', 'text-align':'center'}),
                width=6, lg=3),
        ],
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H2(id='80-degree-days-1', style={'font-size':25, 'color': 'blue', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='Low-below-zero-1', style={'font-size':25, 'color': 'blue', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='80-degree-days-2', style={'font-size':25, 'color': 'darkorange', 'text-align':'center'}),
                width=6, lg=3),
            dbc.Col(
                html.H2(id='Low-below-zero-2', style={'font-size':25, 'color': 'darkorange', 'text-align':'center'}),
                width=6, lg=3),
        ],
    ),
    dbc.Row(
        [
            dbc.Col(
                html.Div([
                    dcc.Graph(id='combined-histogram-max', style={'height':700}),
                ]),
                width = {'size':4},
            ),
            dbc.Col(
                html.Div([
                    dcc.Graph(id='combined-histogram-min', style={'height':700}),
                ]),
                width = {'size': 4},
            )
        ],
        justify='around'
    ),
    dbc.Row(
        [
            dbc.Col(
                html.H3(id='stats-for-year1-1',style={'height':100, 'text-align': 'center'}),
                ),
            dbc.Col(
                html.H3(id='stats-for-year2-2',style={'height':100, 'text-align': 'center'}),
                ),
        ],
        align = 'around'
    ),
    # dbc.Row(
    #     [
    #         dbc.Col(
    #             html.Div([
    #                 dcc.Graph(id='yearly-avg-max-trend', style={'height':700},
    #                     figure = {
    #                         'data': [
    #                             {
    #                                 'x' : df5.index, 
    #                                 'y' : df5['TMAX'],
    #                                 'mode' : 'lines + markers',
    #                                 'name' : 'Max Temp'
    #                             },
    #                             {
    #                                 'x' : df5.index,
    #                                 'y' : annual_max_fit(),
    #                                 'name' : 'trend'
    #                             }
    #                         ],
    #                         'layout': go.Layout(
    #                             xaxis = {'title': 'Date'},
    #                             yaxis = {'title': 'Temp'},
    #                             hovermode = 'closest',    
    #                         ), 
    #                     }
    #                 ),

    #             ]),
    #             width = {'size': 4},
    #         ),
    #         dbc.Col(
    #             html.Div([
    #                 dcc.Graph(id='yearly-avg-min-trend', style={'height':700},
    #                     figure = {
    #                         'data': [
    #                             {
    #                                 'x' : df5.index, 
    #                                 'y' : df5['TMIN'],
    #                                 'mode' : 'lines + markers',
    #                                 'name' : 'Min Temp'
    #                             },
    #                             {
    #                                 'x' : df5.index,
    #                                 'y' : annual_min_fit(),
    #                                 'name' : 'trend'
    #                             }
    #                         ],
    #                         'layout': go.Layout(
    #                             xaxis = {'title': 'Date'},
    #                             yaxis = {'title': 'Temp'},
    #                             hovermode = 'closest',      
    #                         ), 
    #                     }
    #                 ),

    #             ]),
    #             width = {'size':4},
    #         ),
    #     ],
    #     justify='around'
    # ),
    dbc.Row(
        [
            dbc.Col(
                html.Div(
                    html.H3('DENVER MAX TEMPS, 1948-PRESENT'),
                style={'height':100, 'background-color':'lightsilver', 'text-align': 'center'}
                ),
                width = {'size':5},
            ),
            dbc.Col(
                html.Div(
                    html.H3('DENVER MIN TEMPS, 1948-PRESENT'),
                style={'height':100, 'background-color':'lightsilver', 'text-align': 'center'}
                ),
                width = {'size':5}, 
            ),
        ],
         justify='around',
    ),

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
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-3], annual_max_mean_rankings.index[drl-3].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-3], annual_min_mean_rankings.index[drl-3].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-4], annual_max_mean_rankings.index[drl-4].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-4], annual_min_mean_rankings.index[drl-4].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_max_mean_rankings[drl-5], annual_max_mean_rankings.index[drl-5].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2- {:,.1f} Deg F,  {}".format(annual_min_mean_rankings[drl-5], annual_min_mean_rankings.index[drl-5].year)),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),


    # dbc.Row(
    #     [
    #        dbc.Col(
    #             html.Div([
    #                 dcc.Graph(id='all-max-temps',  
    #                     figure = {
    #                         'data': [
    #                             {
    #                                 'x' : df.index, 
    #                                 'y' : allmax_rolling_mean,
    #                                 'mode' : 'lines + markers',
    #                                 'name' : 'Max Temp'
    #                             },
    #                             {
    #                                 'x' : df5.index,
    #                                 'y' : all_max_temp_fit(),
    #                                 'name' : 'trend'
    #                             }
    #                         ],
    #                         'layout': go.Layout(
    #                             xaxis = {'title': 'Date'},
    #                             yaxis = {'title': 'Temp'},
    #                             hovermode = 'closest',
    #                             height = 1000     
    #                         ), 
    #                     }
    #                 ),

    #             ]),
    #             width = {'size': 8, 'offset':2},
    #         ), 
    #     ],
    # ),
    dbc.Row(
        [
            dbc.Col(
                html.H3('Max Temps 1948-Present, 5 Year Moving Avg', style={'height':100, 'text-align': 'center'}),
                ),
        ],
        align = 'around'
    ),
    # dbc.Row(
    #     [
    #        dbc.Col(
    #             html.Div([
    #                 dcc.Graph(id='all-min-temps',  
    #                     figure = {
    #                         'data': [
    #                             {
    #                                 'x' : df.index, 
    #                                 'y' : allmin_rolling_mean,
    #                                 'mode' : 'lines + markers',
    #                                 'name' : 'Max Temp'
    #                             },
    #                             {
    #                                 'x' : df5.index,
    #                                 'y' : all_min_temp_fit(),
    #                                 'name' : 'trend'
    #                             }
    #                         ],
    #                         'layout': go.Layout(
    #                             xaxis = {'title': 'Date'},
    #                             yaxis = {'title': 'Temp'},
    #                             hovermode = 'closest',
    #                             height = 1000     
    #                         ), 
    #                     }
    #                 ),

    #             ]),
    #             width = {'size': 8, 'offset':2},
    #         ), 
    #     ]
    # ),
    dbc.Row(
        [
            dbc.Col(
                html.H3('Min Temps 1948-Present, 5 Year Moving Avg', style={'height':100, 'text-align': 'center'}),
                ),
        ],
        align = 'around'
    ),
    dbc.Row(
        dbc.Col(
            html.Div(id='divider', style={'height':200, 'background-color':'silver'})    
                ),
    ),    
],
fluid = 'True'
)

# @app.callback(Output('graph1', 'figure'),
#               [Input('year-picker', 'value'),
#               Input('param', 'value')])
# def update_figure(selected_year, param):
#     filtered_year = df[df.index.year == selected_year]
#     traces = []
#     if param == max:
#         year_param = filtered_year['TMAX']
#     else:
#         year_param = filtered_year['TMIN']
#     # year_MAXT = filtered_year['TMAX']
#     # year_MINT = filtered_year["TMIN"]

#     traces.append(go.Scatter(
#         y = year_param,
#         name = param
#     ))
#     traces.append(go.Scatter(
#         y = df_norms['DLY-TMAX-NORMAL'],
#         name = "Normal Max T"
#     ))

#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis = {'title': 'DAY'},
#             yaxis = {'title': 'TMAX'},
#             hovermode = 'closest',
#             title = '3 Day Rolling Avg'
#         )
#     }

# @app.callback(Output('graph1', 'figure'),
#               [Input('year-picker1', 'value'),
#                Input('year-picker2', 'value')])
# def update_figure(selected_year1, selected_year2):
#     filtered_year1 = df[df.index.year == selected_year1]
#     filtered_year2 = df[df.index.year == selected_year2]
#     traces = []
#     year1_rolling = filtered_year1['TMAX'].rolling(window=3)
#     year2_rolling = filtered_year2['TMAX'].rolling(window=3)
#     rolling_year1 = year1_rolling.mean()
#     rolling_year2 = year2_rolling.mean()

#     traces.append(go.Scatter(
#         y = rolling_year1,
#         name = selected_year1
#     ))
#     traces.append(go.Scatter(
#         y = rolling_year2,
#         name = selected_year2
#     ))

#     return {
#         'data': traces,
#         'layout': go.Layout(
#             xaxis = {'title': 'YEAR'},
#             yaxis = {'title': 'TMAX'},
#             hovermode = 'closest',
#             title = '3 Day Rolling Avg'
#         )
#     }



# @app.callback(Output('stats-for-year1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_i(selected_year1):
#     return 'Stats for {}'.format(selected_year1)

# @app.callback(Output('stats-for-year2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_j(selected_year2):
#     return 'Stats for {}'.format(selected_year2)

# @app.callback(Output('Maximum-yearly-temp-1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_a(selected_year1):
#     filtered_df1 = df[df.index.year == selected_year1]
#     annual_max_temp1 = filtered_df1['TMAX'].max()
#     return 'Maximum Yearly Temp: {:.0f}'.format(annual_max_temp1)

# @app.callback(Output('Minimum-yearly-temp-1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_b(selected_year1):
#     filtered_df1 = df[df.index.year == selected_year1]
#     annual_min_temp1 = filtered_df1['TMIN'].min()
#     return 'Minimum Yearly Temp: {:.0f}'.format(annual_min_temp1)

# @app.callback(Output('Maximum-yearly-temp-2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_c(selected_year2):
#     filtered_df1 = df[df.index.year == selected_year2]
#     annual_max_temp2 = filtered_df1['TMAX'].max()
#     return 'Maximum Yearly Temp: {:.0f}'.format(annual_max_temp2)

# @app.callback(Output('Minimum-yearly-temp-2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_d(selected_year2):
#     filtered_df1 = df[df.index.year == selected_year2]
#     annual_min_temp2 = filtered_df1['TMIN'].min()
#     return 'Minimum Yearly Temp: {:.0f}'.format(annual_min_temp2)

# @app.callback(Output('90-degree-days-1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_e(selected_year1):
#     filtered_df1 = df[df.index.year == selected_year1]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').max()
#     days_over_90 = (df_max[df_max['TMAX'] >= 90].count()['TMAX'])
#     return 'Total Days Above 90 : {}'.format(days_over_90)

# @app.callback(Output('High-below-freezing-1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_f(selected_year1):
#     filtered_df1 = df[df.index.year == selected_year1]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').max()
#     days_high_below_zero = (df_max[df_max['TMAX'] < 32].count()['TMAX'])
#     return 'Days High Below Freezing : {:.0f}'.format(days_high_below_zero)

# @app.callback(Output('90-degree-days-2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_g(selected_year2):
#     filtered_df1 = df[df.index.year == selected_year2]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').max()
#     days_over_90 = (df_max[df_max['TMAX'] >= 90].count()['TMAX'])
#     return 'Total Days Above 90 : {}'.format(days_over_90)

# @app.callback(Output('High-below-freezing-2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_h(selected_year2):
#     filtered_df1 = df[df.index.year == selected_year2]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').max()
#     days_high_below_zero = (df_max[df_max['TMAX'] < 32].count()['TMAX'])
#     return 'Days High Below Freezing : {:.0f}'.format(days_high_below_zero)

# @app.callback(Output('80-degree-days-1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_m(selected_year1):
#     filtered_df1 = df[df.index.year == selected_year1]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').max()
#     days_over_80 = (df_max[df_max['TMAX'] >= 80].count()['TMAX'])
#     return 'Total Days Above 80 : {}'.format(days_over_80)

# @app.callback(Output('Low-below-zero-1', 'children'),
#               [Input('year-picker1', 'value')])
# def update_layout_n(selected_year1):
#     filtered_df1 = df[df.index.year == selected_year1]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').min()
#     days_low_below_zero = (df_max[df_max['TMIN'] < 0].count()['TMIN'])
#     return 'Days Low Below 0 : {:.0f}'.format(days_low_below_zero)


# @app.callback(Output('80-degree-days-2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_k(selected_year2):
#     filtered_df1 = df[df.index.year == selected_year2]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').max()
#     days_over_80 = (df_max[df_max['TMAX'] >= 80].count()['TMAX'])
#     return 'Total Days Above 80 : {}'.format(days_over_80)

# @app.callback(Output('Low-below-zero-2', 'children'),
#               [Input('year-picker2', 'value')])
# def update_layout_l(selected_year2):
#     filtered_df1 = df[df.index.year == selected_year2]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     df_max = filtered_df1.resample('D').min()
#     days_low_below_zero = (df_max[df_max['TMIN'] < 0].count()['TMIN'])
#     return 'Days Low Below 0 : {:.0f}'.format(days_low_below_zero)

# @app.callback(Output('combined-histogram-max','figure'),
#               [Input('year-picker1', 'value'),
#               Input('year-picker2', 'value')])

# def update_graph_a(selected_year1,selected_year2):
#     filtered_df1 = df[df.index.year == selected_year1]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     filtered_df2 = df[df.index.year == selected_year2]
#     filtered_df2['datetime'] = pd.to_datetime(filtered_df2['DATE'])
#     filtered_df2 = filtered_df2.set_index('datetime')
    
#     trace1 = go.Histogram(
#         x=filtered_df1['TMAX'],
#         opacity=.5,
#         xbins=dict(size=10),
#         name = selected_year1
#     )

#     trace2 = go.Histogram(
#         x=filtered_df2['TMAX'],
#         opacity=.5,
#         xbins=dict(size=10),
#         name = selected_year2
#     )

#     data = [trace1, trace2]

#     fig = go.Figure(
#         data = data,
#         layout = go.Layout(barmode='overlay')
#         )
#     return fig


# # Histogram of minimum daily temps for two selected years
# @app.callback(Output('combined-histogram-min','figure'),
#               [Input('year-picker1', 'value'),
#               Input('year-picker2', 'value')])

# def update_graph_b(selected_year1,selected_year2):
#     filtered_df1 = df[df.index.year == selected_year1]
#     filtered_df1['datetime'] = pd.to_datetime(filtered_df1['DATE'])
#     filtered_df1 = filtered_df1.set_index('datetime')
#     filtered_df2 = df[df.index.year == selected_year2]
#     filtered_df2['datetime'] = pd.to_datetime(filtered_df2['DATE'])
#     filtered_df2 = filtered_df2.set_index('datetime')
    
#     trace1 = go.Histogram(
#         x = filtered_df1['TMIN'],
#         opacity = .5,
#         xbins = dict(size = 10),
#         name = selected_year1
#     )

#     trace2 = go.Histogram(
#         x = filtered_df2['TMIN'],
#         opacity = .5,
#         xbins = dict(size=10),
#         name = selected_year2
#     )

#     data = [trace1, trace2]

#     fig = go.Figure(
#         data = data,
#         layout = go.Layout(barmode='overlay')
#         )
#     return fig

# @app.callback(Output('stats-for-year1-1', 'children'),
#               [Input('year-picker1', 'value'),
#               Input('year-picker2', 'value')])
# def update_layout_o(selected_year1, selected_year2):
#     return 'Max Temps: {} and {}'.format(selected_year1,selected_year2)

# @app.callback(Output('stats-for-year2-2', 'children'),
#               [Input('year-picker2', 'value'),
#               Input('year-picker1', 'value')])
# def update_layout_p(selected_year2, selected_year1):
#     return 'Min Temps: {} and {}'.format(selected_year1,selected_year2)

app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)