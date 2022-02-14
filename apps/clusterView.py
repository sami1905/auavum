import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
from app import app
from textblob_de import TextBlobDE as TextBlob
import plotly.express as px
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords
import nltk
import matplotlib.pyplot as plt
import random
import plotly.graph_objs as go
import numpy as np
import pandas as pd
from apps import summary, profiler


import functions.dataProfiling as dProfile

def show_cluster(cluster_nr, data, listOfFrei, listOfFest, col):
    df= data.loc[data['Cluster'] == cluster_nr]
    df = df.set_index(df.columns[0])
    charts = []
    corr = dProfile.getCorr(df[listOfFest])

    text_file = open('./assets/txt/stopwords.txt', 'r', encoding='utf-8')
    swords = text_file.read()
    text_file.close()
    liste_der_unerwuenschten_woerter = swords.split()
    
    for fest in listOfFest:
        pie_value=df.columns.get_loc(fest)
        charts.append(dbc.Col(html.Div([dcc.Graph(figure = getPie(pie_value, df), style={'margin-top' : '40px'})]), width=6))
                    
    # sentiment
    list_polarity = []
    list_subjektivity = []
    list_countCharts = []

    list_polarity_str = []
    index_str = []

    texts = df[col].values
    summarizeTheText = ""

    
    for text in texts:
        blob = TextBlob(text)
        list_polarity.append(blob.sentiment.polarity)
        list_subjektivity.append(blob.sentiment.subjectivity)
        list_countCharts.append(len(text))
        summarizeTheText = summarizeTheText + text + " "
       

    for index in df.index:
        index_str.append(str(index))

    scatter = px.scatter(df, x=list_polarity, y=list_subjektivity, size=list_countCharts, hover_data=[texts,df.index])
    scatter.update_layout(yaxis_title='Subjektivität', xaxis_title='Polarität')  

    histo = px.histogram(df, x=list_polarity, y= index_str)
    histo2 = px.histogram(df, y= list_polarity_str)
    list_polarity.sort()
    for pol in list_polarity:
        list_polarity_str.append(str(pol))
    pie = px.pie(df, list_polarity_str)

    
    german_stop_words = stopwords.words('german')
    STOPWORDS.update(german_stop_words)
    STOPWORDS.update(liste_der_unerwuenschten_woerter)

    wordcloud = WordCloud(background_color="white",width=1100, height=750).generate(summarizeTheText)
    wc = wordcloud.to_image()
    fig3 = px.imshow(np.array(wc))
    fig3.update_layout(coloraxis_showscale=False)
    fig3.update_layout(height=900, hovermode=False)
    fig3.update_xaxes(showticklabels=False)
    fig3.update_yaxes(showticklabels=False)

    count_values =(len(df.columns)*(len(df.index)))
    percent_float = (df.isnull().sum().sum()/count_values)
    percent_int = round(percent_float*100)

    #sun = px.sunburst(df, path=listOfFest)




    children = [
        dcc.Store(id='clusterdata', storage_type='memory', data=df.to_json(date_format='iso', orient='split')),
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
                        dbc.Col(dbc.Button("Zurück", color="secondary", style={'position' : 'relative', 'left': '-25px'}, id={"type":"dynamic-back-btn", "index": cluster_nr}),width=1),
                        dbc.Col(html.Div([
                            html.H1('Cluster-Dashboard'),
                            html.P('Cluster ' + str(cluster_nr), style={'margin-bottom': '5px'}, className='card-text1')
                        ]),width=10),
                        dbc.Col(width=1),
                    ])
                ])
            ], className='deskriptiv-card'),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Allgemeine Informationen:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            dbc.Row([
                                html.P('Anzahl der Zeilen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                                html.P(str(len(df.index)), className='card-text2'),
                            ], style={'margin-left':'3px'}),
                            dbc.Row([
                                html.P('Anzahl der Spalten gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                html.P(str(len(df.columns)), className='card-text2'),
                            ], style={'margin-left':'3px'}),
                            dbc.Row([
                                html.P('Anzahl Zellen gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                html.P(str(count_values), className='card-text2')
                            ], style={'margin-left':'3px'}),
                            dbc.Row([
                                html.P('Anzahl leerer Zellen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                                html.P(str(df.isnull().sum().sum()) + ' (' + str(percent_int) + '%)', className='card-text2')
                            ], style={'margin-left':'3px'}),
                            dbc.Row([
                                    html.P('Ausgewähltes Merkmal (Spalte): ' , className='card-text2', style={'font-weight': 'bold'}),
                                    html.P(col, className='card-text2')
                                    ], style={'margin-left':'3px'})
                        ])
                    ], style={"width": "max", "height": "max"}, className='deskriptiv-card'),
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Text Summarizer:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            html.Div(summary.layout(summarizeTheText))
                        ])
                    ],style={"width": "max", "height": "max"}, className='deskriptiv-card')],width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Korrelation:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            dcc.Graph(id="corr", style={'margin': '2%'}, figure = corr)
                        ])
                    ], className='deskriptiv-card'),
                    ],width=4),
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Word-Cloud:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            
                            dcc.Graph(id="cloud", style={'height': '470px', "margin":"0", "padding":"0"}, figure = fig3),
                        ])
                    ], className='deskriptiv-card'), width = 4)
            ]),

            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Merkmale (Spalten):", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            html.P('Wähle ein Merkmal (Spalte):' , className='card-text2', style={'font-weight': 'bold'}),
                            dcc.Dropdown(id='prof-dropdown', 
                                    	    options=[{'label': i, 'value': i} for i in listOfFest], 
                                            value=listOfFest[0], 
                                            clearable=False,
                                            searchable=False,
                                            className='dropdown'),
                    html.Div([], id="prof"),
                        ])
                    ], className='deskriptiv-card'), width = 6),
                dbc.Col(dbc.Card([
                    dbc.CardBody([
                        html.H4("Sentiment-Analyse:", style={'text-align': 'left'}),
                        html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                        html.P("Polarität",style={'margin': '4%'}),
                        dcc.Graph(id="scatter-graph", style={'margin': '2%'}, figure = scatter),
                        dbc.Row([
                            dcc.Graph(id="histo-graph", style={'margin': '2%'}, figure = histo),
                            dcc.Graph(id="histo-graph2", style={'margin': '2%'}, figure = histo2),

                        ]),
                        dcc.Graph(id="pie-graph", style={'margin': '2%'}, figure = pie),
                        
                        
                            
                        ])
                ], className='deskriptiv-card'),width=6)   
            ])           
                    
        ])
    ]

    return children


def getPie(col, data):
    fig = px.pie(data_frame=data, names=data.columns[col])
    return fig

@app.callback(Output('prof', 'children'),
               [Input('prof-dropdown', 'value'),
               Input('clusterdata', 'data')])
def update_profile_content(value, data):
    if data is not None:
        df = pd.read_json(data, orient='split')           
        print(value)
        return profiler.profile(df, value)
    else:
        return None





