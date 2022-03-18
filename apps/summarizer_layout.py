from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px
from app import app

import numpy as np
from apps import summary


layout=dbc.Container([
    

# if main_data == None
    html.Div([
        dbc.Row([
        dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
        dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
        dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
        ] ,className='header'),
        html.H1('Oops!', style={'font-size':'100px', 'margin':'40px'}),
        html.Img(src='../assets/img/404.png', height='400px'),
        html.H1('404 - PAGE NOT FOUND', style={'font-size':'30px', 'margin':'30px'}),
        html.P('Die gesuchte Seite scheint nicht zu existieren. Kehre zurück zur Startseite.', className='card-text1', style={'margin-bottom':'20px'}),
        dcc.Link(dbc.Button('Zurück zur Startseite', color='secondary', className='upload-button'), href='/')
    ],  id={'type':'errorView', 'index':4}, className='alert-wrapper', style={'display':'none'}),
    
    # Main-content
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
            dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
            dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
        ] ,className='header'),

        dbc.Row([
            dbc.Col([], width=3),
            dbc.Col(html.Img(src='assets/img/progress4of4.png', className='progress-img'), width=6),
            dbc.Col(html.Div(id='output-alert-prepare', style={'display':'none'}, className='upload-alert'),width=3)
        ], className='progress-row'),

        
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dcc.Link(dbc.Button("Zurück", color="secondary", style={'position' : 'relative', 'left': '-25px'}), href="/verfahren-waehlen"),width=1),
                    dbc.Col(html.Div([
                        html.H1('Schritt 4: Ergebnis erhalten'),
                        html.P('Lasse Dir eine Zusammenfassung der in einer ausgewählten Spalte enthaltenden Freitext ausgeben.', style={'margin-bottom': '5px'}, className='card-text1')
                    ]),width=10),
                    dbc.Col(width=1),
                ])
            ])
        ], className='deskriptiv-card'),
        
        dbc.Card([
            
                dbc.Tabs(
                    [
                        dbc.Tab(label="Text Summarizer", tab_id="tab-summarizer"),
                        dbc.Tab(label="Daten", tab_id="tab-data"),
                    ],
                    id="card-tabs",
                    active_tab="tab-summarizer",
                    style={'background': '#f2f2f263'}
                ),
            dbc.CardBody([
                    
                    
                    html.H4("Text Summarizer", style={'text-align': 'left'}),
                    html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                    html.Div([
                        html.P('Wähle die Freitexte aus, die zusammegefasst werden sollen:' , className='card-text2', style={'font-weight': 'bold'}),
                        dcc.Dropdown(id='text-dropdown', 
                                    	    options=[{'label': '-', 'value': '-'}], 
                                            value='-', 
                                            clearable=False,
                                            searchable=False,
                                            className='dropdown')

                    ], style={'text-align': 'left'}),
                    
                    html.Div([], id="summarized-text"),
                    
            ],id="tab_summarizer", style={'text-align': 'left'}),
            
            dbc.CardBody([
                html.H4("Daten", style={'text-align': 'left'}),
                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                html.Div(id='show-summarizer-data')
            ], id="tab_data2")
        ], className='deskriptiv-card')
    ], id="summarizer"),
], className='content', fluid=True)

@app.callback(Output('show-summarizer-data', 'children'), Input('main_data_after_preperation', 'data'))
def show_data(data):
    if data is not None:
        df = pd.read_json(data, orient='split')
        df = df.fillna('Keine Angaben')
        children = [html.Div([dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)], style={'text-align': 'left'})]

        return children
    return None

@app.callback(
    [Output("tab_summarizer", "style"), Output("tab_data2", "style")], [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    style1 = {'display':'block'}
    style2 = {'display':'none'}

    if active_tab == 'tab-summarizer':
        return style1, style2
    
    else: 
        return style2, style1





@app.callback([Output({'type':'errorView', 'index':4}, 'style'), Output('summarizer', 'style')],
               [Input('main_data_after_preperation', 'data'),
               Input('listOfFest', 'data'),
               Input('listOfFrei', 'data')])
def error2(main_data, d1, d2):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    
    if main_data is None or d1 is None or d2 is None:
        return style1, style2
    
    else:
        return style2, style1

@app.callback(Output('text-dropdown', 'options'),
               [Input('listOfFrei', 'data')])
def update_text_dropdown(cols):
    options=[{'label':'-', 'value':'-'}]
    if cols is not None:
        
        for col in cols:
            options.append({'label':'{}'.format(col, col), 'value':col})
            
    return options

@app.callback(Output('summarized-text', 'children'),
               [Input('text-dropdown', 'value'),
               Input('main_data_after_preperation', 'data')])
def update_text_dropdown(value, data):
    
    if data is not None:
        df = pd.read_json(data, orient='split')
        
        if value != "-":
            df = df.dropna(subset=[value])
            
            texts = df[value].values
            summarizeTheText = ""

    
            for text in texts:
                summarizeTheText = summarizeTheText + text + " "
                        
            return summary.layout(summarizeTheText)
        else:
            return None
            
    return None