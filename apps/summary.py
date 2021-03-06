from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from app import app
from summarizer.sbert import SBertSummarizer
import pandas as pd

summary_model  =  SBertSummarizer ('distiluse-base-multilingual-cased-v1') 

def layout(text):
    
    
    children = dbc.Container([
        dcc.Store(id='summary-data', storage_type='memory', data=text),

        html.Div([
            html.P('Gib an, in wie vielen Sätzen die Freitexte zusammengefasst werden sollen:' , className='card-text2', style={'margin-top':'10px'}),
                                
            dcc.RangeSlider(
                id='count_sent',
                min=1, max=10, step=1,
                marks={1: '1', 2: '2', 3:'3', 4:'4', 5:'5', 6:'6', 7:'7', 8:'8', 9:'9', 10: '10'},
                value=[0],
            ),

        ], style={"width":"80%", "text-align":"left", 'margin-top':'20px'}),
            
        html.Div([
            
        ], id="summary-content")
            
    ],style={'text-align':'left'}, fluid=True)
    return children

@app.callback([Output("summary-content", "children"),
                Output("summary","data")], 
                [Input("count_sent", "value"),
                Input('summary-data', 'data')]
)
def get_summary(k, data):
    if k[0] != 0:
        summary =summarize(data, k[0])
        children = dbc.Row([
            html.P('Zusammenfassung: ', className='card-text2', style={'font-weight': 'bold'}),
            html.P(summary, className='card-text2'),
        ], style={'margin-left':'3px', 'text-align':'left'})

        listSum=[summary]




        return children, listSum
    else:
        return None, None


def summarize(text, k):
    result = summary_model(text, num_sentences=k)
    full = ''.join(result)
    return full