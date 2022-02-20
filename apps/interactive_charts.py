from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import plotly.express as px
from app import app
import dash
import json


layout=dbc.Container([
    html.Div([
        html.P('Einstellungen' , className='card-text2', style={'font-weight': 'bold', 'margin-top':'10px'}),
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.P('Diagramm-Art:', className='card-text2', style={'margin': '5px 0 0 10px'}),
                    dcc.Dropdown(id='chart-type', 
                        options=[{'label': 'Sunburst ', 'value': 1},
                                {'label': 'Icicle', 'value': 2},
                                {'label': 'Treemap', 'value': 3},
                                {'label': 'Parallel Categories', 'value': 4}], 
                        value=1, 
                        clearable=False,
                        searchable=False,
                        className='dropdown',
                        style={'font-size': '14px', 'width': '300px'})
                ]), width=3),
            dbc.Col(
                html.Div([
                    html.P('Ebenen: ' , className='card-text2'),
                    dcc.Dropdown(id='ebenen', options= [{'label':'-', 'value':'-'}], value=[], placeholder = "Füge eine oder mehrere Ebenen hinzu...", multi=True, className='dropdown', style={'font-size':'14px'})
                ]),width=9)
        ]),
    ]),
    html.Div([
        html.P('Diagramm' , className='card-text2', style={'font-weight': 'bold', 'margin-top':'30px'}),
        html.Div([], id='interactive-figure', style={'text-align':'center', 'margin':'0 auto'})
    ])       
], fluid=True, style={'text-align': 'left'})


@app.callback(
    Output('ebenen', 'options'),
    [Input('ebenen', 'value')],
    [State('listOfFest', 'data'),
    State('ebenen', 'options')]
)
def update_ebenen(values, listOfFest, options):
    options = []
    if listOfFest is not None:
        for col in listOfFest:
            options.append({'label':col, 'value': col})
        
        
    return options
   

@app.callback(
    Output('interactive-figure', 'children'),
    [Input('ebenen', 'value'),
    Input('chart-type', 'value')],
    [State('main_data_after_preperation', 'data')]
)
def get_figur(values, chart_type, data):
    listofCols = []
    fig = {}
    if values == []:
        return None
    else:

        if data is not None:
            for (i, value) in enumerate(values):
                listofCols.append(value)
            
            df = pd.read_json(data, orient='split')
            df = df.fillna('Keine Angaben')
            df = df[listofCols]

            if chart_type == 1:
                fig = px.sunburst(df, path=listofCols, width=900, height=900)
            elif chart_type == 2:
                fig = px.icicle(df, path=listofCols, width=900, height=900)
            elif chart_type == 3:
                fig = px.treemap(df, path=listofCols, width=900, height=900)
            elif chart_type == 4:
                fig = px.parallel_categories(df, width=900, height=900)

        return dcc.Graph(figure = fig)


