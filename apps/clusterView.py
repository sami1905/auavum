import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
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
from apps import summary, profiler, interactive_charts, chart_dashboard, sentiment


import functions.dataProfiling as dProfile

def show_cluster(cluster_nr, data, listOfFrei, listOfFest, col, listOfTopics):
    listOfClusterTopic =  pd.read_json(listOfTopics, orient='split')

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
    ind = df.index.values
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
                    ]),
                    dbc.Row([
                        dbc.Col(width=11),
                        dbc.Col(
                            dbc.DropdownMenu([
                                dbc.DropdownMenuItem(".CSV", id="download-3", n_clicks=0), 
                                dbc.DropdownMenuItem(".XLSX", id="download-4", n_clicks=0)
                            ], label="Download", group=True, id="download2", color="dark", style={'display':'None'}), width=1),
                    ], style={'text-align':'center', 'margin':'40px 0px 0px 0px'}),
                    dcc.Download(id="download-cluster-csv"),
                    dcc.Download(id="download-cluster-xlsx"),
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
                        ], style={'text-align' : 'left'})
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
                            html.H4("Topic Modeling:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            
                            dcc.Graph(id="cloud", style={'height': '470px', "margin":"0", "padding":"0"}, figure = fig3),
                            html.Div([
                                html.P('Top-10-Themen: ' , className='card-text2', style={'font-weight': 'bold'}),
                                dbc.Row([
                                    dbc.Col(html.Div([
                                        dbc.Row([
                                            dbc.Col(html.P('1: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[0]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[0], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),
                                                
                                        dbc.Row([
                                            dbc.Col(html.P('2: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[1]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[1], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),
                                                
                                        dbc.Row([
                                            dbc.Col(html.P('3: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[2]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[2], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),

                                        dbc.Row([
                                            dbc.Col(html.P('4: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[3]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[3], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),

                                        dbc.Row([
                                            dbc.Col(html.P('5: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[4]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[4], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),

                                    ]),width=5),
                                    dbc.Col(html.Div([
                                        dbc.Row([
                                            dbc.Col(html.P('6: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[5]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[5], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),
                                               
                                        dbc.Row([
                                            dbc.Col(html.P('7: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[6]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[6], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),
                                                
                                        dbc.Row([
                                            dbc.Col(html.P('8: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[7]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[7], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),

                                        dbc.Row([
                                            dbc.Col(html.P('9: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[8]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[8], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),

                                        dbc.Row([
                                            dbc.Col(html.P('10: ', className='card-text2', style={'font-weight': 'bold'}),width=4),
                                            dbc.Col(html.P(str(listOfClusterTopic.index.values.tolist()[9]) + " (" + str(round(listOfClusterTopic['tfidf'].tolist()[9], 5)) + ")", className='card-text2'))
                                        ], style={'margin-left':'20px'}),


                                    ]),width=5),
                                ])
                            ], style={'text-align' : 'left'})
                        ])
                            
                    ], className='deskriptiv-card'), width = 4)
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Diagramm-Dashboard:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            html.Div([chart_dashboard.layout], style={'text-align': 'left'})
                        ])
                ], className='deskriptiv-card'),width=12)   
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
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Interaktive Diagramme:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            html.Div([interactive_charts.layout], style={'text-align': 'left'})
                        ])
                    ], className='deskriptiv-card'), width = 6)
            ]),
            dbc.Row([
                dbc.Col(
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Sentiment-Analyse:", style={'text-align': 'left'}),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            html.Div(sentiment.layout(texts, ind))
                            
                        ])
                ], className='deskriptiv-card'),width=12)   
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
        return profiler.profile(df, value)
    else:
        return None


@app.callback(Output('download2', 'style'),
               [Input('summary', 'data')])
def showDownload(data):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    if data is not None:
        return style1
    else:
        return style2


@app.callback([Output('download-cluster-csv', 'data'),
            Output('download-cluster-xlsx', 'data'),
            Output('download-3', 'n_clicks'),
            Output('download-4', 'n_clicks')],
            Input('download-3', 'n_clicks'),
            Input('download-4', 'n_clicks'),
            State('clusterdata', 'data'),
            State('listOfTopics', 'data'),
            State('summary', 'data'),
            State('listOfSentiment', 'data'),
            State('choosen-col', 'value'),
            State('sentiment-split', 'data'),
            prevent_initial_call=True,)
def download(csv, xlsx, data, listOfTopics, summary, listOfSentiment, col, checkbox):
    df = pd.read_json(data, orient='split')
    df_sent= pd.read_json(listOfSentiment, orient='split')
    df_sent=df_sent.set_index('Index')
    print(df_sent)

    df_raw = pd.DataFrame({'Index': df.index.values.tolist(),
                        'Text': df[col].values.tolist()})

    
    if checkbox == [1]:
        df_splited = pd.DataFrame(columns = df.columns)
        for i, p in df_raw.itertuples(index=False):

            sentence_token = nltk.tokenize.sent_tokenize(p)
            print(sentence_token)
            for index in df.index.values.tolist():
                if index == i:
                    for t in sentence_token:
                        data = df.loc[i]
                        data[col]=t
                        df_splited=df_splited.append(data)

        print(df_splited)

    else:
        df_splited = df.copy()
    
    
    df_splited['Summarization (' + col + ')'] = summary[0]
    df_splited['Polarität(' + col + ')'] = df_sent['Polarität']
    df_splited['Subjektivität(' + col + ')'] = df_sent['Subjektivität']
    print(df_splited)

    cluster = df_splited['Cluster'].values.tolist()

    if csv:
        return dcc.send_data_frame(df_splited.to_csv, "cluster"+str(cluster[0])+".csv"), None, 0, 0
    
    elif xlsx:
        return dcc.send_data_frame(df_splited.to_excel, "cluster"+str(cluster[0])+".xlsx", sheet_name="Cluster"), None, 0, 0
    
    else:
        return None, None, 0,0


