import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import sqlite3
from dash.dependencies import Input, Output
import time
# import datetime
from datetime import datetime

cnx = sqlite3.connect('denvertemps.db')

app = dash.Dash(__name__)

# df = pd.read_sql_query("SELECT * FROM temperatures", cnx)
df = pd.read_csv('../../stapleton.csv')






df['datetime']= pd.to_datetime(df['DATE'])
df = df.set_index('datetime')
# print(df.index.year)

years = []
for YEAR in df.index.year.unique():
    years.append({'label':(YEAR), 'value':YEAR})


app.layout = html.Div([
    html.Div(
        className="app-header",
        children=[
            html.Div('Denver Temperatures', className="app-header--title"),
        ]
    ),
    html.Div(
        children=html.Div(
             html.H3(children='1948-Present',style={'text-align': 'center'})
        )
    ),
    html.Div([
        html.H3('Denver Max Daily Temp', style={'text-align': 'center', 'color': 'blue'}),
        dcc.Graph(id='graph'),
        
            html.Div([
                dcc.Dropdown(id='year-picker1',options=years),
            ],
            style={'width': '48%', 'display': 'inline-block'}), 
            html.Div([
                dcc.Dropdown(id='year-picker2',options=years),
            ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
            
    ]),
    html.Div([
        html.H3(id='stats-for-year1')
    ]),
    html.Div([
        html.Div(
            style={'color': 'red', 'font-size':20, 'width': '24%', 'display':'inline-block'},
            id='90-degree-days-1',
            children='90-degree-days-1:'        
        )
    ])

])

@app.callback(Output('graph', 'figure'),
              [Input('year-picker1', 'value'),
               Input('year-picker2', 'value')])
def update_figure(selected_year1, selected_year2):
    filtered_df1 = df[df.index.year == selected_year1]
    filtered_df2 = df[df.index.year == selected_year2]
    traces = []
    traces.append(go.Scatter(
            # x=filtered_df1[filtered_df1.index.month],
            y=filtered_df1['TMAX'],
            mode='lines',
            name=selected_year1
        ))
    traces.append(go.Scatter(
            # x=filtered_df2['DATE'],
            y=filtered_df2['TMAX'],
            mode='lines',
            name=selected_year2
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'YEAR'},
            yaxis={'title': 'TMAX'},
            hovermode='closest'
        )
    }

@app.callback(Output('90-degree-days-1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_a(selected_year1):
    filtered_df1 = df[df.index.year == selected_year1]
    # td = datetime.now().day
    # tm = datetime.now().month
    # ty = datetime.now().year
    # dfd = df[df.index.day == td]
    # dfdm = dfd[dfd.index.month == tm]
    # dfdmy = dfdm[dfdm.index.year == ty]
    # print(dfdmy)
    annual_max_temp1 = filtered_df1['TMAX'].max()
    return 'Maximum Yearly Temp: {:.0f}'.format(annual_max_temp1)

@app.callback(Output('stats-for-year1', 'children'),
              [Input('year-picker1', 'value')])
def update_layout_b(selected_year1):
    return 'Stats for {}'.format(selected_year1)


if __name__ == '__main__':
    app.run_server(port=8124) 