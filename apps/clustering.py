from importlib.resources import contents
import time
from app import app
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
import numpy as np
import torch
import apps.clusterView as cView
import dash
import json
import plotly.figure_factory as ff
import scipy.cluster.hierarchy as sch
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
from sentence_transformers import SentenceTransformer
import xlsxwriter
import io 

#embedding
BERTmodel = SentenceTransformer('distiluse-base-multilingual-cased-v1') #erst complete

# topic-modeling
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


## Dimension Reduction
import umap.umap_ as umap
from sklearn.manifold import TSNE

#word tokenizer
from nltk.tokenize import word_tokenize

#lemmatization
import spacy
lemma = spacy.load('de_core_news_md')
#stemmer
from nltk.stem import PorterStemmer
porter = PorterStemmer()

#stopwords
from nltk.corpus import stopwords
text_file = open('./assets/txt/stopwords.txt', 'r', encoding='utf-8')
swords = text_file.read()
text_file.close()
liste_der_unerwuenschten_woerter = swords.split()

german_stop_words = liste_der_unerwuenschten_woerter #+ stopwords.words('german')


layout=dbc.Container([
    dcc.Store(id='vectors', storage_type='memory'),
    dcc.Store(id='clusters', storage_type='memory'), 
    dcc.Store(id='clustered_df', storage_type='memory'),    
    #dcc.Store(id='clustered-data', storage_type='memory'),
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
    ],  id={'type':'errorView', 'index':7}, className='alert-wrapper', style={'display':'none'}),
    
    # Main-content
    html.Div([
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
                            html.P('Führe für ausgewählte Freitexte eine hierarchischen Clusteranalyse mithilfe von agglomerativen Berechnungen durch. Wähle hierzu Merklmal (Spalte) und die gewünschte Cluster-Anzahl und erhalte die Datenprofile der berechneten Cluster. Unter dem Tab "Daten" kannst Du Dir jederzeit die geclusterten Daten nach Cluster und Merkmalen (Spalten) filtern und anzeigen lassen. ', style={'margin-bottom': '5px'}, className='card-text1')
                        ]),width=10),
                        dbc.Col(width=1),
                    ])
                ])
            ], className='deskriptiv-card'),
            dbc.Card([
                dbc.CardHeader(
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Clustering-Analyse", tab_id="tab-1_clustering"),
                            dbc.Tab(label="Daten", tab_id="tab-2_clustering"),
                        ],
                        id="card-tabs_clustering",
                        active_tab="tab-1_clustering",
                    )
                ),
                dbc.CardBody([
                    html.H4("Clustering-Analyse", style={'text-align': 'left'}),
                    html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                    dbc.Row([
                        dbc.Col(width=11),
                        dbc.Col(
                            dbc.DropdownMenu([
                                dbc.DropdownMenuItem(".CSV", id="download-1", n_clicks=0), 
                                dbc.DropdownMenuItem(".XLSX", id="download-2", n_clicks=0)
                            ], label="Download", group=True, id="download", color="dark", style={'display':'None'}), width=1),
                    ], style={'text-align':'center', 'margin':'40px 0px 0px 0px'}),
                    
                    dcc.Download(id="download-clustering-csv"),
                    dcc.Download(id="download-clustering-xlsx"),

                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                html.P("Wähle das Merkmal für die Durchführung der Clustering-Analyse:" , className="card-text2", style={"font-weight": "bold", "margin":"20px 0 10px 0"}),
                                dcc.Dropdown(id="choosen-col", options= [{'label':'-', 'value':'-'}], value='-', searchable=False, clearable=False, className='dropdown'),

                                html.Div(id="dendro", children=[], style={"margin":"20px 0"})
                            ]), width=7),
                        dbc.Col(
                            html.Div([
                                html.P('Wähle die Cluster-Anzahl:' , className='card-text2', style={"font-weight": "bold", "margin":"20px 0"}),
                                dcc.RangeSlider(
                                    id='count_clusters',
                                    min=2, max=24, step=1,
                                    marks={2: '2', 3:' ', 4:'4', 5:' ', 6:'6', 7:' ', 8:'8', 9:' ', 10: '10', 11:' ', 12: '12', 13:' ', 14:'14', 15: ' ', 16:'16', 17: ' ', 18: '18', 19: ' ', 20:'20', 21: ' ', 22:'22', 23: ' ', 24: '24'},
                                    value=[1],
                                ),
                                html.Div(id='show-cluster-plot', children=None, style={"margin": "20px 0", "width":"650px", "text-align":"center"}),
                            ], style={"width":"80%", "text-align":"left"}), width=5)
                    ]),
                    html.Div(id='show-clusters', children=None, style={"margin": "10px 0"})
                ],id="tab_1_clustering", style={"margin": "10px 0"}),
                
                dbc.CardBody([
                    html.H4("Daten", style={'text-align': 'left'}),
                    html.Hr(style={'margin': '0 0 30px 0', 'padding':'0'}),
                    dbc.Row([
                        dbc.Col(html.Div([], id='data-info'), width= 4),
                        dbc.Col(
                            html.Div([
                                html.H2('Einstellungen'),
                                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                                
                                html.P('Filtern nach Cluster: ' , className='card-text2', style={'font-weight': 'bold'}),
                                dcc.Dropdown(id='filter-cluster', 
                                                        options=[{'label': 'Alle', 'value': 'Alle'}], 
                                                        value='Alle', 
                                                        clearable=False,
                                                        searchable=False,
                                                        className='dropdown',
                                                        style={'font-size':'14px'}),
                                html.P('Angezeigte Merkmale (Spalten): ' , className='card-text2', style={'font-weight': 'bold'}),
                                dcc.Dropdown(id='filter-cols', options= [{'label':'-', 'value':'-'}], value=[], multi=True, placeholder='Wähle oder suche Spalten, die entfernt werden sollen...', className='dropdown', style={'font-size':'14px'})
                            ]), width= 8)

                    ]),
                    html.Div(id='cluster-table', children=[])
                ], id="tab_2_clustering")
            ], id="dendro-card"),
            
        ], id='analysis', style={'display':'block'}),

        html.Div([], id='clusterview', style={'display':'none'})

    ], id='clustering-content'),
], className='content', fluid=True)

@app.callback(Output('choosen-col', 'options'),
            [Input('main_data_after_preperation', 'data'), Input('choosen-col', 'options')],
            [State('listOfFest', 'data')])
def update_dropdowns(data, options, listOfFest):
    if data is not None:
        df = pd.read_json(data, orient='split')
        df = df.fillna('Keine Angaben')
        df = df.set_index(df.columns[0])
        if listOfFest != None:
            for col in listOfFest:
                df = df.drop(columns=[col])
        i=0
        for col in df.columns:
            options.append({'label':col, 'value':col})
    return options

@app.callback([Output("tab_1_clustering", "style"), 
                Output("tab_2_clustering", "style")], 
                [Input("card-tabs_clustering", "active_tab")])
def tab_content(active_tab):
    style1 = {'display':'block'}
    style2 = {'display':'none'}

    if active_tab == 'tab-1_clustering':
        return style1, style2
    
    else: 
        return style2, style1

@app.callback([Output('dendro', 'children'), Output('vectors', 'data')],
            [Input('choosen-col', 'value')],
            [State('main_data_after_preperation', 'data')])
def show_dendro(col, data):

    print("Start 'show_dendro'")
    start = time.perf_counter()
    if data is not None and col != "-":
        df = pd.read_json(data, orient='split')
        df = df.set_index(df.columns[0])
        df = df.dropna(subset=[col])
        sentences = df[col].tolist()
            
        print("Start 'transformation' after: ")
        finished = time.perf_counter()
        print(f'{round(finished-start, 2) } second(s)')
        vectors = new_bert(sentences)
        print("Beenden 'transformation' after: ")
        finished = time.perf_counter()
        print(f'{round(finished-start, 2) } second(s)')
        labels=[]
        for i in df.index:
            labels.append(i)
            
        df=df.reset_index()
        print("Start 'get_dendro' after: ")
        finished = time.perf_counter()
        print(f'{round(finished-start, 2) } second(s)')
        dendro = get_Dendro(vectors, labels)
        print("Beenden 'get_dendro' after: ")
        finished = time.perf_counter()
        print(f'{round(finished-start, 2) } second(s)')
            
        return dcc.Graph(figure=dendro), vectors
    else:
        return None, None

@app.callback([Output('data-info', 'children'), Output('cluster-table', 'children')],
        Input('main_data_after_preperation', 'data'),
        Input('clusters', 'data'),
        Input('filter-cols', 'value'),
        Input('choosen-col', 'value'),
        Input('filter-cluster', 'value'))
def show_table(data, clusters, show_cols, col, filter_cluster):
    if data is not None:
        df = pd.read_json(data, orient='split')
        
        if col != "-":
            df = df.dropna(subset=[col])
        
        if show_cols != []:
            df=df[show_cols]
        if clusters is None:
            df['Cluster'] = 1
            count_cluster = 1
        
        else:
            df['Cluster'] = clusters
            count_cluster = len(list(dict.fromkeys(clusters)))

        
        if filter_cluster != 'Alle':
            df = df.loc[df['Cluster'] == filter_cluster]
        
        count_values =(len(df.columns)*(len(df.index)))
        percent_float = (df.isnull().sum().sum()/count_values)
        percent_int = round(percent_float*100)

        children_info = [
                    html.Div([
                        html.H2('Informationen'),
                        html.Hr(style={'margin': '0 0 5px 0', 'padding':'0'}),
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
                                ], style={'margin-left':'3px'}),
                        dbc.Row([
                            html.P('Anzahl Cluster: ' , className='card-text2', style={'font-weight': 'bold'}),
                            html.P(str(count_cluster), className='card-text2')
                        ], style={'margin-left':'3px'}),

                    ]
                )
        ]
                    
        children_table = [
            html.H2('Tabelle', style={'margin': '20px 0 5px 0', 'padding':'0'}),
            html.Hr(style={'margin': '0 0 20px 0', 'padding':'0'}),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)
        ]
        
        return children_info, children_table
    
    else: return None, None

@app.callback([Output('download-clustering-csv', 'data'),
            Output('download-clustering-xlsx', 'data'),
            Output('download-1', 'n_clicks'),
            Output('download-2', 'n_clicks')],
            Input('download-1', 'n_clicks'),
            Input('download-2', 'n_clicks'),
            State('clustered_df', 'data'),
            State('listOfTopics', 'data'),
            prevent_initial_call=True,)
def download(csv, xlsx, data, listOfTopics):
    df = pd.read_json(data, orient='split')
    df_names = []
    df_list = []
    x=1

    for top in listOfTopics:
        df_list.append(pd.read_json(top, orient='split'))
        df_names.append('Cluster ' + str(x))
        x=x+1

    if csv:
        return dcc.send_data_frame(df.to_csv, "clustering.csv"), None, 0, 0
    
    elif xlsx:
        output = io.BytesIO()
        writer = pd.ExcelWriter(output, engine="xlsxwriter")
        df.to_excel(writer, sheet_name="Clustering")
        for num,dftoExcel in enumerate(df_list):
           copytoexcel = pd.DataFrame(dftoExcel)
           copytoexcel.to_excel(writer, sheet_name=df_names[num])
        writer.save()

        return None, dcc.send_bytes(output.getvalue(), "clustering.xlsx"), 0, 0
    
    else:
        return None, None, 0,0



@app.callback([Output('filter-cluster', 'options'),
            Output('filter-cols', 'options'), Output('filter-cols', 'value')],
             Input('main_data_after_preperation', 'data'),
            Input('clusters', 'data'),
            Input('filter-cols', 'value'))
def update_drops(data, clusters, value):
    options1 = []
    options2 = [{'label':"Alle", 'value':"Alle"}]
    if data is not None:
        df = pd.read_json(data, orient='split')
        listOfCols = df.columns

        if value == []:
            value = listOfCols

        for col in listOfCols:
            options1.append({'label':col, 'value':col})

        
        if clusters != None:
            clusters = list(dict.fromkeys(clusters))
            clusters.sort()
            for clu in clusters:
                options2.append({'label':clu, 'value':clu})

    return options2, options1, value




@app.callback([Output('show-clusters', 'children'),
                Output('clusters', 'data'),
                Output('show-cluster-plot', 'children'),
                Output('listOfTopics', 'data'),
                Output('download', 'style'),
                Output('clustered_df', 'data')],
            [Input('count_clusters', 'value'),
            Input('vectors', 'data')],
            [State('main_data_after_preperation', 'data'),
            State('choosen-col', 'value')])
def show_clusters(k, vectors, data, col):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    
    if data is not None and col != "-":
        df = pd.read_json(data, orient='split')
        df = df.dropna(subset=[col])
        if k[0] < 2:
            scatter = plot_2d(vectors, None, df.index.values.tolist())
            return None, None, dcc.Graph(figure=scatter), None, style2, None
        
        else:
            cluster = get_Clusters(k[0], vectors)
            scatter = plot_2d(vectors, cluster, df.index.values.tolist())
            df["Cluster"] = cluster+1
            tfidf, listOfTopics  = getTopics(df, col)
            clusters = list(dict.fromkeys(cluster))
            clusters.sort()
            children = []
        
        
            for clu in clusters:
                is_open = False
                clu = clu+1
                if clu == 1:
                    is_open = True

                top5topics = tfidf[clu-1][:10]
                df_c= df.loc[df['Cluster'] == clu]
                count_values =(len(df_c.columns)*(len(df_c.index)))
                percent_float = (df_c.isnull().sum().sum()/count_values)
                percent_int = round(percent_float*100)
                new_collapse = html.Div([
                        html.H2(["Cluster " + str(clu)], id={'type':'dynamic-btn', 'index': int(clu)},
                            n_clicks=0,
                            style={'background': '#f2f2f2', 'color' : '#3c4143', 'width':'max',
                            "border-bottom": "2px #3c414350 solid", "padding": "20px 10px", "margin" : "0"}
                        ),
                        dbc.Collapse(
                        html.Div([
                                html.H2('Informationen'),
                                html.Hr(style={'margin': '0 0 5px 0', 'padding':'0'}),
                                dbc.Row([
                                    dbc.Col(html.Div([
                                        dbc.Row([
                                            html.P('Anzahl der Zeilen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                                            html.P(str(len(df_c.index)), className='card-text2'),
                                        ], style={'margin-left':'3px'}),
                                        dbc.Row([
                                            html.P('Anzahl der Spalten gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                            html.P(str(len(df_c.columns)), className='card-text2'),
                                        ], style={'margin-left':'3px'}),
                                        dbc.Row([
                                            html.P('Anzahl Zellen gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                            html.P(str(count_values), className='card-text2')
                                        ], style={'margin-left':'3px'}),
                                        dbc.Row([
                                            html.P('Anzahl leerer Zellen gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                            html.P(str(df_c.isnull().sum().sum()) + ' (' + str(percent_int) + '%)', className='card-text2')
                                        ], style={'margin-left':'3px'})

                                        ]),width=4),
                                    dbc.Col(html.Div([
                                            html.P('Top-10-Themen: ' , className='card-text2', style={'font-weight': 'bold'}),
                                            dbc.Row([
                                                dbc.Col(html.Div([
                                                    dbc.Row([
                                                        dbc.Col(html.P('1: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[0]) + " (" + str(round(top5topics['tfidf'].tolist()[0], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),
                                                    
                                                    dbc.Row([
                                                        dbc.Col(html.P('2: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[1]) + " (" + str(round(top5topics['tfidf'].tolist()[1], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),
                                                    
                                                    dbc.Row([
                                                        dbc.Col(html.P('3: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[2]) + " (" + str(round(top5topics['tfidf'].tolist()[2], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),

                                                    dbc.Row([
                                                        dbc.Col(html.P('4: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[3]) + " (" + str(round(top5topics['tfidf'].tolist()[3], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),

                                                    dbc.Row([
                                                        dbc.Col(html.P('5: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[4]) + " (" + str(round(top5topics['tfidf'].tolist()[4], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),

                                                ]),width=4),
                                                dbc.Col(html.Div([
                                                    dbc.Row([
                                                        dbc.Col(html.P('6: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[5]) + " (" + str(round(top5topics['tfidf'].tolist()[5], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),
                                                    
                                                    dbc.Row([
                                                        dbc.Col(html.P('7: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[6]) + " (" + str(round(top5topics['tfidf'].tolist()[6], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),
                                                    
                                                    dbc.Row([
                                                        dbc.Col(html.P('8: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[7]) + " (" + str(round(top5topics['tfidf'].tolist()[7], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),

                                                    dbc.Row([
                                                        dbc.Col(html.P('9: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[8]) + " (" + str(round(top5topics['tfidf'].tolist()[8], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),

                                                    dbc.Row([
                                                        dbc.Col(html.P('10: ', className='card-text2', style={'font-weight': 'bold'}), width=3),
                                                        dbc.Col(html.P(str(top5topics.index.values.tolist()[9]) + " (" + str(round(top5topics['tfidf'].tolist()[9], 5)) + ")", className='card-text2'))
                                                    ], style={'margin-left':'20px'}),


                                                ]),width=4),
                                            ])

                                        ]), width=8)
                                ], style={'margin':'0 0 25px 3px'}),
                                dbc.Button(["Mehr zu Cluster " + str(clu) + "..."], id={'type':'dynamic-more-btn', 'index': int(clu)},
                                    color="secondary",
                                    n_clicks=0,
                                ),

                            ]), style={'background': '#3c414330', 'color' : '#3c4143', 'width':'max','margin':'-2px 0 0 0', "padding":"15px", "border-bottom": "2px #3c414350 solid"},
                            id={'type':'cluster-collapse', 'index': int(clu)},
                            is_open=is_open
                        ),
                        
                    ])

                children.append(new_collapse)
            
            
            return children, df["Cluster"], dcc.Graph(figure=scatter), listOfTopics, style1, df.to_json(date_format='iso', orient='split')
    else:
        return None, None, None, None, style2, None

   
@app.callback(
    Output({'type':'cluster-collapse', 'index': MATCH}, 'is_open'),
    [Input({'type':'dynamic-btn', 'index': MATCH}, 'n_clicks')],
    State({'type':'cluster-collapse', 'index': MATCH}, 'is_open'),
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback([Output({'type':'errorView', 'index':7}, 'style'), Output('clustering-content', 'style')],
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

@app.callback([Output('clusterview', 'children'),
                Output('clusterview', 'style'), Output('analysis', 'style'),
                Output({'type':'dynamic-more-btn', 'index': ALL}, 'n_clicks'),
                Output({"type":"dynamic-back-btn", "index": ALL}, 'nclicks')],
                [Input({'type':'dynamic-more-btn', 'index': ALL}, 'n_clicks'),
                Input({"type":"dynamic-back-btn", "index": ALL}, 'n_clicks')],
            [State('listOfFrei', 'data'),
            State('listOfFest', 'data'),
            State('listOfTopics', 'data'),
            State('main_data_after_preperation', 'data'),
            State('clusters', 'data'),
            State('choosen-col', 'value')])
def show_clusterview(clicks, back_clicks, listOfFrei, listOfFest, listOfTopics, data, clusters, col):
    view=[]
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    if data is not None and col != "-":
        df = pd.read_json(data, orient='split')
        df_cluster = df.dropna(subset=[col])
        df_cluster["Cluster"] = clusters
    
        input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    
        if "index" in input_id:
            cluster_nr = json.loads(input_id)["index"]
            for n, i in enumerate(clicks):
                if i != 0:
                    clicks[n] = 0
                    view = cView.show_cluster(cluster_nr, df_cluster, listOfFrei, listOfFest, col, listOfTopics[cluster_nr-1])

        if view != []:
            return view, style1, style2, clicks, back_clicks 
    
        for n, i in enumerate(back_clicks):
            if i != 0:
                back_clicks[n] = 0
                return view, style2, style1, clicks, back_clicks
        else:
            return view, style2, style1, clicks, back_clicks
 
            
    
    else:
        return view, style2, style1, clicks, back_clicks


def get_Dendro(vectors, labels):
    

    #dendro1 = sch.dendrogram(sch.linkage(vectors, method='complete'), color_threshold=0.0, above_threshold_color='black')
    
    # plt.savefig('D:\Benutzer\Eigene Dateien\SMT\Thesis\Experimente\Clustering\Curr_Model2_Complete')
    #  # Initialize figure by creating upper dendrogram
  
    dendro = ff.create_dendrogram(vectors, orientation='bottom', labels=labels, linkagefun=lambda x: sch.linkage(vectors, "average", "cosine"))
    # for i in range(len(dendro['data'])):
    #     dendro['data'][i]['yaxis'] = 'y2'
        
    # # Create Side Dendrogram
    # dendro_side = ff.create_dendrogram(vectors, orientation='right', linkagefun=lambda x: sch.linkage(vectors, "average", "cosine"))
    # for i in range(len(dendro_side['data'])):
    #     dendro_side['data'][i]['xaxis'] = 'x2'
            
    # # Add Side Dendrogram Data to Figure
    # for data in dendro_side['data']:
    #     dendro.add_trace(data)
        
    # # Add Side Dendrogram Data to Figure
    # for data in dendro_side['data']:
    #     dendro.add_trace(data)
        
    # # Create Heatmap
    # dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    # dendro_leaves = list(map(int, dendro_leaves))

    # data_dist = pdist(vectors)
    # heat_data = squareform(data_dist)
    # heat_data = heat_data[dendro_leaves,:]
    # heat_data = heat_data[:,dendro_leaves]

    # heatmap = [
    #     go.Heatmap(
    #         x = dendro_leaves,
    #         y = dendro_leaves,
    #         z = heat_data,
    #         colorscale = 'Blues'
    #     )]
        
    # heatmap[0]['x'] = dendro['layout']['xaxis']['tickvals']
    # heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # # Add Heatmap Data to Figure
    # for data in heatmap:
    #     dendro.add_trace(data)

    # # Edit Layout
    # dendro.update_layout({'width':1000, 'height':1000,
    #                         'showlegend':False, 'hovermode': 'closest',
    #                         })

    # # Edit xaxis
    # dendro.update_layout(xaxis={'domain': [.15, 1],
    #                                     'mirror': False,
    #                                     'showgrid': False,
    #                                     'showline': False,
    #                                     'zeroline': False,
    #                                     'ticks':""})
    # # Edit xaxis2
    # dendro.update_layout(xaxis2={'domain': [0, .15],
    #                                     'mirror': False,
    #                                     'showgrid': False,
    #                                     'showline': False,
    #                                     'zeroline': False,
    #                                     'showticklabels': False,
    #                                     'ticks':""})

    # # Edit yaxis
    # dendro.update_layout(yaxis={'domain': [0, .85],
    #                                     'mirror': False,
    #                                     'showgrid': False,
    #                                     'showline': False,
    #                                     'zeroline': False,
    #                                     'showticklabels': False,
    #                                     'ticks': ""
    #                             })
    # # Edit yaxis2
    # dendro.update_layout(yaxis2={'domain':[.825, .975],
    #                                     'mirror': False,
    #                                     'showgrid': False,
    #                                     'showline': False,
    #                                     'zeroline': False,
    #                                     'showticklabels': False,
    #                                     'ticks':""})   

    return dendro

def get_Clusters(k, vectors):
    Hclustering = AgglomerativeClustering(n_clusters=k, affinity='cosine', linkage='average')
    Hclustering.fit(vectors)
    
    return Hclustering.labels_

def new_bert(sentences):
    filtered_sentences = []
    
    for sent in sentences:
        # tokenization
        sent_token = word_tokenize(sent)

        #removing special characters
        tokens_without_sc = []
        for token in sent_token:
            word = ''.join(e for e in token if e.isalnum())
            if word != '':
                tokens_without_sc.append(word)
  
        #removing stopwords
        tokens_without_sc_an_sw = [word for word in tokens_without_sc if not word.lower() in german_stop_words]
            
        #stemming
        stemmed_tokens_without_sc_and_sw = []
        for word in tokens_without_sc_an_sw:
            stemmed_tokens_without_sc_and_sw.append(porter.stem(word))

        curr_sent = (" ").join(stemmed_tokens_without_sc_and_sw)
        filtered_sentences.append(curr_sent)

    vecs = BERTmodel.encode(filtered_sentences, show_progress_bar=True)
    vectors = vecstoXd(vecs, 20, 2)
    
    return vectors

def vecstoXd(vecs, nneighbors, x):
    #reducer = umap.UMAP(random_state=42, n_neighbors=len(vecs[0]), n_components=2, metric='cosine', min_dist=0.5)
    #reducer = umap.UMAP(random_state=42, n_neighbors=nneighbors, n_components=x, metric='cosine', min_dist=0.8)
    #vec2d= reducer.fit_transform(vecs)

    reducer = TSNE(n_components=2, verbose=10, random_state=41, metric="cosine")

    vec2d=reducer.fit_transform(vecs)
        
    return vec2d

def plot_2d(vectors, clusterLabels, index):
    result = pd.DataFrame(vectors, columns=['x','y'])
    result["Index"] = index
   
    if clusterLabels is not None:

        result['Cluster'] = clusterLabels+1
        result["Cluster"] = result["Cluster"].astype(str)
        fig = px.scatter(result, x="x", y="y", color='Cluster', symbol="Cluster", color_continuous_scale=["red", "orange", "yellowgreen", "green", "olive", "blue", "navy", "grey"], custom_data=['Index', 'Cluster'])
        fig.update_traces(hovertemplate="<br>".join([
            "X: %{x}",
            "Y: %{y}",
            "Index: %{customdata[0]}",
            "Cluster: %{customdata[1]}"
            ])
        ) 

    else:
        fig = px.scatter(result, x="x", y="y", custom_data=['Index'])

        fig.update_traces(hovertemplate="<br>".join([
            "X: %{x}",
            "Y: %{y}",
            "Index: %{customdata[0]}"
        ]))        

    #fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
    #fig.layout.paper_bgcolor = 'rgba(0,0,0,0)'


    return fig

def getTopics(df, col):

    size_cluster = len(df['Cluster'].value_counts())
    
    raw_docs = []
    
    for clu in range(1, size_cluster+1):
        
        cluster = df[df['Cluster'] == clu]
        d = cluster[col].tolist()
        doc=''
        for s in d:
            doc = doc + ' ' + s
        raw_docs.append(doc)
       
    docs=[]
    
    for sent in raw_docs:
        
        # tokenization
        sent_token = word_tokenize(sent)

        #removing special characters
        tokens_without_sc = []
        for token in sent_token:
            w = ''.join(e for e in token if e.isalnum())
            if w != '':
                tokens_without_sc.append(w)
       
        #removing stopwords
        tokens_without_sc_an_sw = [word for word in tokens_without_sc if not word.lower() in german_stop_words]
        
        #lemmatization
        #lemma_tokens_without_sc_and_sw = []
        #for w in tokens_without_sc_an_sw:
        #    doc = lemma(w)
        #    lemma_token = ' '.join([x.lemma_ for x in doc]) 
        #    lemma_tokens_without_sc_and_sw.append(lemma_token)
        
        curr_sent = (" ").join(tokens_without_sc_an_sw)
        docs.append(curr_sent)
    cv=CountVectorizer()
    word_count_vector=cv.fit_transform(docs)
    
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True) 
    tfidf_transformer.fit(word_count_vector)
    
    # print idf values 
    df_idf = pd.DataFrame(tfidf_transformer.idf_, index=cv.get_feature_names(),columns=["idf_weights"]) 
    # sort ascending 
    df_idf.sort_values(by=['idf_weights'])
    
    
    # count matrix 
    count_vector=cv.transform(docs) 
    # tf-idf scores 
    tf_idf_vector=tfidf_transformer.transform(count_vector)
    
    feature_names = cv.get_feature_names() 
    results = []
    #get tfidf vector for first document 
    for fe in tf_idf_vector:
        first_document_vector=fe 
        df = pd.DataFrame(first_document_vector.T.todense(), index=feature_names, columns=["tfidf"])
        
        results.append(df.sort_values(by=["tfidf"],ascending=False))
    #print the scores 

    listOfTopics = []
    for top in results:
        listOfTopics.append(top.to_json(date_format='iso', orient='split'))
        
    return results, listOfTopics

