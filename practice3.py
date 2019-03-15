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
df1 = pd.concat([df_old, df_new], ignore_index=True)
df1['datetime'] = pd.to_datetime(df1['DATE'])
df1 = df1.set_index('datetime')

df['datetime'] = pd.to_datetime(df['DATE'])
df = df.set_index('datetime')

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

df_da_cd = (df5[-(current_year_indexer):]).mean()
df_da_cd['combined'] = (df_da_cd['TMAX'] + df_da_cd['TMIN']) / 2
df5['combined'] = (df5['TMAX'] + df5['TMIN']) / 2
df10['combined'] = (df10['TMAX'] + df10['TMIN']) / 2


df_da['combined'] = (df_da['TMAX'] + df_da['TMIN']) / 2
# add current decade to decade list
df10.loc['2010'] = df_da_cd
# sorts decade combined temps
decade_combined_rankings = df10['combined'].sort_values(axis=0, ascending=True)
decade_max_rankings = df10['TMAX'].sort_values(axis=0, ascending=True)
decade_min_rankings = df10['TMIN'].sort_values(axis=0, ascending=True)
arl = decade_combined_rankings.size

# sorts annual mean temps
annual_max_mean_rankings = df5['TMAX'].sort_values(axis=0, ascending=True)
annual_min_mean_rankings = df5['TMIN'].sort_values(axis=0, ascending=True)
annual_combined_rankings = df5['combined'].sort_values(axis=0, ascending=True)
drl = annual_max_mean_rankings.size
print(type(annual_combined_rankings))
print(decade_combined_rankings.iloc[1])
# current year stats
cy_max = df_new.loc[df_new['TMAX'].idxmax()]
cy_min = df_new.loc[df_new['TMIN'].idxmin()]
cy_max_mean = df_new['TMAX'].mean()
cy_min_mean = df_new['TMIN'].mean()

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
                html.Div(
                    html.H(id='stats',style={'text-align':'center'}),
                ),
            ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6(id='yearly-high/low')
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6(id='mean-max/min'),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6(id='days-above-100/below-0')
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6(id='days-above-90/high-below-0'),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6(id='days-above-80/below-32')
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6(id='days-above-normal/below-normal'),
            ]),
            width={'size':6},
            style={'text-align':'center'}
        ),
    ]),
    # dbc.Row([
    #     dbc.Col(
    #         html.Div([
    #             html.H6("Yearly High: {:,.1f} Deg F, {}".format(cy_max['TMAX'], cy_max['DATE'])),
    #         ]),
    #         width={'size':6},
    #         style={'text-align':'center'}
    #     ),
    #     dbc.Col(
    #         html.Div([
    #             html.H6("Yearly Low: {:,.1f} Deg F, {}".format(cy_min['TMIN'], cy_min['DATE'])),
    #         ]),
    #         width={'size':6},
    #         style={'text-align':'center'}
    #     ),
    # ]),
    # dbc.Row([
    #     dbc.Col(
    #         html.Div([
    #             html.H6("YTD Mean Max: {:,.1f} Deg F".format(cy_max_mean)),
    #         ]),
    #         width={'size':6},
    #         style={'text-align':'center'}
    #     ),
    #     dbc.Col(
    #         html.Div([
    #             html.H6("YTD Mean Min: {:,.1f} Deg F".format(cy_min_mean)),
    #         ]),
    #         width={'size':6},
    #         style={'text-align':'center'}
    #     ),
    # ]),
    # dbc.Row([
    #     dbc.Col(
    #         html.Div([
    #             html.H6("Days High Above Normal: {} ".format(dmaxan)),
    #         ]),
    #         width={'size':6},
    #         style={'text-align':'center'}
    #     ),
    #     dbc.Col(
    #         html.Div([
    #             html.H6("Days Low Above Normal: {} ".format(dminan)),
    #         ]),
    #         width={'size':6},
    #         style={'text-align':'center'}
    #     ),
    # ]),
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
                    html.H4('Decade Rankings-Mean Max ',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Decade Rankings-Mean Min',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Decade Rankings-Overall',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
        ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(decade_max_rankings.index[arl-1],decade_max_rankings.iloc[arl-1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(decade_min_rankings.index[arl-1],decade_min_rankings.iloc[arl-1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(decade_combined_rankings.index[arl-1],decade_combined_rankings.iloc[arl-1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(decade_max_rankings.index[arl-2],decade_max_rankings.iloc[arl-2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(decade_min_rankings.index[arl-2],decade_min_rankings.iloc[arl-2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(decade_combined_rankings.index[arl-2],decade_combined_rankings.iloc[arl-2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(decade_max_rankings.index[arl-3],decade_max_rankings.iloc[arl-3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(decade_min_rankings.index[arl-3],decade_min_rankings.iloc[arl-3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(decade_combined_rankings.index[arl-3],decade_combined_rankings.iloc[arl-3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(decade_max_rankings.index[arl-4],decade_max_rankings.iloc[arl-4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(decade_min_rankings.index[arl-4],decade_min_rankings.iloc[arl-4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(decade_combined_rankings.index[arl-4],decade_combined_rankings.iloc[arl-4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(decade_max_rankings.index[arl-5],decade_max_rankings.iloc[arl-5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(decade_min_rankings.index[arl-5],decade_min_rankings.iloc[arl-5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(decade_combined_rankings.index[arl-5],decade_combined_rankings.iloc[arl-5])),
            ]),
            width={'size':4},
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
                html.H6("1. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-1].year, annual_max_mean_rankings[drl-1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-1].year, annual_min_mean_rankings[drl-1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-1].year, annual_combined_rankings[drl-1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-2].year, annual_max_mean_rankings[drl-2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-2].year, annual_min_mean_rankings[drl-2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-2].year, annual_combined_rankings[drl-2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-3].year, annual_max_mean_rankings[drl-3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-3].year, annual_min_mean_rankings[drl-3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-3].year, annual_combined_rankings[drl-3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-4].year, annual_max_mean_rankings[drl-4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-4].year, annual_min_mean_rankings[drl-4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-4].year, annual_combined_rankings[drl-4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-5].year, annual_max_mean_rankings[drl-5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-5].year, annual_min_mean_rankings[drl-5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-5].year, annual_combined_rankings[drl-5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("6. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-6].year, annual_max_mean_rankings[drl-6])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-6].year, annual_min_mean_rankings[drl-6])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-6].year, annual_combined_rankings[drl-6])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("7. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-7].year, annual_max_mean_rankings[drl-7])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-7].year, annual_min_mean_rankings[drl-7])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-7].year, annual_combined_rankings[drl-7])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("8. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-8].year, annual_max_mean_rankings[drl-8])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-8].year, annual_min_mean_rankings[drl-8])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-8].year, annual_combined_rankings[drl-8])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("9. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-9].year, annual_max_mean_rankings[drl-9])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-9].year, annual_min_mean_rankings[drl-9])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-9].year, annual_combined_rankings[drl-9])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("10. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[drl-10].year, annual_max_mean_rankings[drl-10])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[drl-10].year, annual_min_mean_rankings[drl-10])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[drl-10].year, annual_combined_rankings[drl-10])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4('Coolest Years-Mean Max ',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Coolest Years-Mean Min',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
            dbc.Col(
                html.Div([
                    html.H4('Coolest Years-Overall',style={'color': 'black','font-size':20}),
                ]),
                width={'size':4},
                style={'height':30, 'text-align':'center'} 
            ),
        ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[0].year, annual_max_mean_rankings[0])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[0].year, annual_min_mean_rankings[0])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("1. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[0].year, annual_combined_rankings[0])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[1].year, annual_max_mean_rankings[1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[1].year, annual_min_mean_rankings[1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("2. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[1].year, annual_combined_rankings[1])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[2].year, annual_max_mean_rankings[2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[2].year, annual_min_mean_rankings[2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("3. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[2].year, annual_combined_rankings[2])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[3].year, annual_max_mean_rankings[3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[3].year, annual_min_mean_rankings[3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("4. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[3].year, annual_combined_rankings[3])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[4].year, annual_max_mean_rankings[4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[4].year, annual_min_mean_rankings[4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("5. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[4].year, annual_combined_rankings[4])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("6. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[5].year, annual_max_mean_rankings[5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[5].year, annual_min_mean_rankings[5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("6. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[5].year, annual_combined_rankings[5])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("7. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[6].year, annual_max_mean_rankings[6])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[6].year, annual_min_mean_rankings[6])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("7. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[6].year, annual_combined_rankings[6])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("8. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[7].year, annual_max_mean_rankings[7])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[7].year, annual_min_mean_rankings[7])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("8. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[7].year, annual_combined_rankings[7])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("9. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[8].year, annual_max_mean_rankings[8])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[8].year, annual_min_mean_rankings[8])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("9. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[8].year, annual_combined_rankings[8])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
    ]),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H6("10. {} - {:,.1f} Deg F".format(annual_max_mean_rankings.index[9].year, annual_max_mean_rankings[9])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10. {} - {:,.1f} Deg F".format(annual_min_mean_rankings.index[9].year, annual_min_mean_rankings[9])),
            ]),
            width={'size':4},
            style={'text-align':'center'}
        ),
        dbc.Col(
            html.Div([
                html.H6("10. {} - {:,.1f} Deg F".format(annual_combined_rankings.index[9].year, annual_combined_rankings[9])),
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

@app.callback(Output('yearly-high/low', 'children'),
              [Input('year-picker', 'value'),
              Input('param', 'value')])
def update_layout_b(selected_year, param):
    filtered_year = df[df.index.year == selected_year]
    yearly_max = filtered_year.loc[filtered_year['' + param + ''].idxmax()]
    yearly_min = filtered_year.loc[filtered_year['' + param + ''].idxmin()]
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
    filtered_year = df1[df1.index.year == selected_year]
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

# days max above normal
# dmaxan = 0
# i = 0
# while i < df_new['TMAX'].count():
#     if df_new.loc[i]['TMAX'] > df_norms_max.loc[i]['DLY-TMAX-NORMAL']:
#         dmaxan = dmaxan + 1
#         i = i + 1
#     else:i = i + 1

# # day min above normal
# dminan = 0
# i = 0
# while i < df_new['TMIN'].count():
#     if df_new.loc[i]['TMIN'] > df_norms_min.loc[i]['DLY-TMIN-NORMAL']:
#         dminan = dminan + 1
#         i = i + 1
#     else:i = i + 1

app.layout = html.Div(body)

if __name__ == "__main__":
    app.run_server(port=8050, debug=True)