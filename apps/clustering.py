
import time
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from app import app
import umap.umap_ as umap
import torch
import apps.clusterView as cView
import dash
import json
import plotly.figure_factory as ff
from app import vectorizer
import scipy.cluster.hierarchy as sch
import plotly.graph_objects as go
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
import plotly.express as px
from transformers import AutoTokenizer, AutoModel
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
token_model = AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')




layout=dbc.Container([
    dcc.Store(id='vectors', storage_type='memory'),
    dcc.Store(id='clusters', storage_type='memory'),    
    dcc.Store(id='clustered-data', storage_type='memory'),
    # if main_data == None
    html.Div([
        dbc.Row([
        dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height="40px"), href='/'), width=1),
        dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
        dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height="40px"), className='header_logo_bwi', width=1)
        ] ,className='header'),
        html.H1("Oops!", style={'font-size':'100px', 'margin':'40px'}),
        html.Img(src='../assets/img/404.png', height="400px"),
        html.H1("404 - PAGE NOT FOUND", style={'font-size':'30px', 'margin':'30px'}),
        html.P("Die gesuchte Seite scheint nicht zu existieren. Kehre zurück zur Startseite.", className="card-text1", style={'margin-bottom':'20px'}),
        dcc.Link(dbc.Button("Zurück zur Startseite", color="secondary", className='upload-button'), href='/')
    ], id='error-clustering', className="alert-wrapper", style={'display':'none'}),
    
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
                                min=2, max=18, step=1,
                                marks={2: '2', 3:' ', 4:'4', 5:' ', 6:'6', 7:' ', 8:'8', 9:' ', 10: '10', 11:' ', 12: '12', 13:' ', 14:'14', 15: ' ', 16:'16', 17: ' ', 18: '18'},
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
        sentences = []
        for val in df[col]:
            sentences.append(val)
            
        print("Start 'transformation' after: ")
        finished = time.perf_counter()
        print(f'{round(finished-start, 2) } second(s)')
        vectors = new_transformation(sentences)
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

@app.callback([Output('filter-cluster', 'options'),
            Output('filter-cols', 'options'), Output('filter-cols', 'value')],
             Input('main_data_after_preperation', 'data'),
            Input('clusters', 'data'),
            Input('filter-cols', 'value'))
def update_drops(data, clusters, value):
    options1 = []
    options2 = [{'label':"Alle", 'value':"Alle"}]
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
                Output('clustered-data', 'data'),
                Output('show-cluster-plot', 'children')],
            [Input('main_data_after_preperation', 'data'),
            Input('choosen-col', 'value'), Input('count_clusters', 'value'), Input('vectors', 'data')])
def show_clusters(data, col, k, vectors):
    if data is not None and col != "-" and k[0] > 1:
        df = pd.read_json(data, orient='split')
        df = df.dropna(subset=[col])

        # if vectors is not None:
        #     vectors = json.dumps(vectors)

       
        cluster = get_Clusters(k[0], vectors)
        scatter = plot_2d(vectors, cluster)
        df["Cluster"] = cluster+1

        clusters = list(dict.fromkeys(cluster))
        clusters.sort()
        children = []
        
        
        for clu in clusters:
            is_open = False
            clu = clu+1
            if clu ==1:
                is_open = True
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
                            ], style={'margin-left':'3px'}),
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
        
        
        return children, df["Cluster"], df.to_json(date_format='iso', orient='split'), dcc.Graph(figure=scatter)
    else:
        return None, None, None, None

   
@app.callback(
    Output({'type':'cluster-collapse', 'index': MATCH}, 'is_open'),
    [Input({'type':'dynamic-btn', 'index': MATCH}, 'n_clicks')],
    State({'type':'cluster-collapse', 'index': MATCH}, 'is_open'),
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback([Output('clusterview', 'children'),
                Output('clusterview', 'style'), Output('analysis', 'style'),
                Output({'type':'dynamic-more-btn', 'index': ALL}, 'n_clicks'),
                Output({"type":"dynamic-back-btn", "index": ALL}, 'nclicks')],
                [Input({'type':'dynamic-more-btn', 'index': ALL}, 'n_clicks'),
                Input({"type":"dynamic-back-btn", "index": ALL}, 'n_clicks')],
            [State('listOfFrei', 'data'),
            State('listOfFest', 'data'),
            State('main_data_after_preperation', 'data'),
            State('clustered-data', 'data'),
            State('choosen-col', 'value')])
def show_clusterview(clicks, back_clicks, listOfFrei, listOfFest, data, df_cluster, col):
    if df_cluster is not None:
        df_cluster = pd.read_json(df_cluster, orient='split')
    
    view=[]
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    df = pd.read_json(data, orient='split')
    if col != '-':
        df = df.dropna(subset=[col])
    input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    
    if "index" in input_id:
        cluster_nr = json.loads(input_id)["index"]
        for n, i in enumerate(clicks):
            if i != 0:
                clicks[n] = 0
                view = cView.show_cluster(cluster_nr, df_cluster, listOfFrei, listOfFest, col)

    if view != []:
        return view, style1, style2, clicks, back_clicks 
    
    for n, i in enumerate(back_clicks):
        if i != 0:
            back_clicks[n] = 0
            return view, style2, style1, clicks, back_clicks 
            
    
    else:
        return view, style2, style1, clicks, back_clicks



def get_Dendro(vectors, labels):

    # Initialize figure by creating upper dendrogram
  
    dendro = ff.create_dendrogram(vectors, orientation='bottom', labels=labels, linkagefun=lambda x: sch.linkage(x, "complete", "euclidean"))
    for i in range(len(dendro['data'])):
        dendro['data'][i]['yaxis'] = 'y2'
        
    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(vectors, orientation='right')
    for i in range(len(dendro_side['data'])):
        dendro_side['data'][i]['xaxis'] = 'x2'
            
    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        dendro.add_trace(data)
        
    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        dendro.add_trace(data)
        
    # Create Heatmap
    dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    dendro_leaves = list(map(int, dendro_leaves))

    data_dist = pdist(vectors)
    heat_data = squareform(data_dist)
    heat_data = heat_data[dendro_leaves,:]
    heat_data = heat_data[:,dendro_leaves]

    heatmap = [
        go.Heatmap(
            x = dendro_leaves,
            y = dendro_leaves,
            z = heat_data,
            colorscale = 'Blues'
        )]
        
    heatmap[0]['x'] = dendro['layout']['xaxis']['tickvals']
    heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # Add Heatmap Data to Figure
    for data in heatmap:
        dendro.add_trace(data)

    # Edit Layout
    dendro.update_layout({'width':1000, 'height':1000,
                            'showlegend':False, 'hovermode': 'closest',
                            })

    # Edit xaxis
    dendro.update_layout(xaxis={'domain': [.15, 1],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'ticks':""})
    # Edit xaxis2
    dendro.update_layout(xaxis2={'domain': [0, .15],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'showticklabels': False,
                                        'ticks':""})

    # Edit yaxis
    dendro.update_layout(yaxis={'domain': [0, .85],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'showticklabels': False,
                                        'ticks': ""
                                })
    # Edit yaxis2
    dendro.update_layout(yaxis2={'domain':[.825, .975],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'showticklabels': False,
                                        'ticks':""})   

    return dendro

def get_Clusters(k, vectors):
    Hclustering = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='complete')
    Hclustering.fit(vectors)
    return Hclustering.labels_

def transformation(sentences):
    print("in old_transformation Funktion")
    vectorizer.bert(sentences)
    vectors = vectorizer.vectors

    return vectors


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def new_transformation(sentences):
    #listfosents=[]
    # for sent in sentences:
    #     text_tokens = word_tokenize(sent)
    #     tokens_without_sw = [word for word in text_tokens if not word in STOPWORDS]

    #     listfosents.append((" ").join(tokens_without_sw))


    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = token_model(**encoded_input)

    # Perform pooling. In this case, max pooling.
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    vecs = sentence_embeddings
    print(len(vecs[0]))
    print(len(vecs[1]))
    reducer = umap.UMAP(random_state=42, n_neighbors=len(vecs[0]), n_components=2, metric='cosine')
    vec2d= reducer.fit_transform(vecs)
    print(vecs)
    print(vec2d)

    return vec2d



def plot_2d(vectors, clusterLabels):    
    result = pd.DataFrame(vectors, columns=['x','y'])
    result['labels'] = clusterLabels+1
    print(result)
    print(clusterLabels)
    
    # fig, ax = plt.subplots(figsize=(20, 10))
    outliers = result.loc[result.labels == -1, :]
    clustered = result.loc[result.labels != -1, :]
    
    # plt.colorbar()

    #fig1 = px.scatter(outliers, x="x", y="y")

    fig = px.scatter(clustered, x="x", y="y", color='labels')
    #fig3 = go.Figure(data=fig1.data + fig2.data)

    return fig
    

       

    





