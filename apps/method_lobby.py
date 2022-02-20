import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import pandas as pd
from app import app
import functions.getTable as tablesFuncs


layout = dbc.Container([
    
    dcc.Store(id='cur_data', storage_type='session'),

# if main_data == None
    html.Div([
        dbc.Row([
        dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
        dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=2),
        dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
        ] ,className='header'),
        html.H1('Oops!', style={'font-size':'100px', 'margin':'40px'}),
        html.Img(src='../assets/img/404.png', height='400px'),
        html.H1('404 - PAGE NOT FOUND', style={'font-size':'30px', 'margin':'30px'}),
        html.P('Die gesuchte Seite scheint nicht zu existieren. Kehre zurück zur Startseite.', className='card-text1', style={'margin-bottom':'20px'}),
        dcc.Link(dbc.Button('Zurück zur Startseite', color='secondary', className='upload-button'), href='/')
    ],  id={'type':'errorView', 'index':1}, className='alert-wrapper', style={'display':'none'}),
    
    # Main-content
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
            dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=2),
            dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
        ] ,className='header'),

        dbc.Row([
            dbc.Col([], width=3),
            dbc.Col(html.Img(src='assets/img/progress3of4.png', className='progress-img'), width=6),
            dbc.Col(html.Div(id='output-alert-prepare', style={'display':'none'}, className='upload-alert'),width=3)
        ], className='progress-row'),

        
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dcc.Link(dbc.Button('Zurück', color='secondary', style={'position' : 'relative', 'left': '-25px'}), href='/daten-vorbereiten'),width=1),
                    dbc.Col(html.Div([
                        html.H1('Schritt 3: Verfahren wählen'),
                        html.P('Wähle ein Verfahren mit dem die Auswertung und Analyse durchgeführt werden soll.', style={'margin-bottom': '5px'}, className='card-text1')
                    ]),width=2),
                    dbc.Col(width=1),
                ])
            ])
        ], className='lobby-card'),
        dbc.Card([
            html.Div([
                html.H2('Deskriptive Auswertung'),
                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                html.P('Die deskriptive Auswertung ermöglicht es Dir, Deine Daten durch verschiedene grafische Darstellungen übersichtlich zu visualisieren und zu ordnen. So erhältst Du eine anschauliche und leicht überblickbare Darstellung Deiner umfangreichen Dateninhalte.', style={'margin-bottom': '5px'}, className='card-text1'),
            
            ], style={'margin':'20px', 'text-align':"left"}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.Row([
                            dbc.Col(dbc.CardImg(src='assets/img/profiling200x150.png', top=True, style={'border-right': '1px #3c414333 solid'}),width=3),
                            dbc.Col(dbc.CardBody([
                                    html.H4('Data-Profiling', className='card-title'),
                                    html.P('Lass Dir ein Profil zu den Merkmalen (Spalten) ausgeben.', className='card-text3'),
                                    dbc.Row([
                                        dbc.Col(width=11),
                                        dbc.Col(dcc.Link(dbc.Button('Auswählen', color='secondary', style={'font-size' : '14px'}), href='/profiling'),width=1),
                                    ],style={'position':'absolute', 'bottom':'0', 'left':'15px'})
                                ], className='method-body'), width=9)
                            ])
                    ], className='method-card'), width=4),
                    dbc.Col(dbc.Card([
                        dbc.Row([
                        dbc.Col(dbc.CardImg(src='assets/img/deskriptiv200x150.png', top=True, style={'border-right': '1px #3c414333 solid'}),width=3),
                        dbc.Col(dbc.CardBody([
                                html.H4('Diagramm-Dashboard', className='card-title'),
                                html.P(
                                    'Erstelle Dein eigenes Diagramm-Dashboard zu Deinen hochgeladenen Daten.',
                                    className='card-text3',
                                ),
                                dbc.Row([
                                    dbc.Col(width=11),
                                    dbc.Col(dcc.Link(dbc.Button('Auswählen', color='secondary', style={'font-size' : '14px'}), href='/diagramm-dashboard'),width=1),
                                ],style={'position':'absolute', 'bottom':'0', 'left':'15px'})
                        ], className='method-body'), width=9)
                        ])
                    ], className='method-card'), width=4),
                    
                    dbc.Col(dbc.Card([
                        dbc.Row([
                        dbc.Col(dbc.CardImg(src='assets/img/sunburst200x150.png', top=True, style={'border-right': '1px #3c414333 solid'}),width=3),
                        dbc.Col(dbc.CardBody([
                                html.H4('Interaktive Diagramme', className='card-title'),
                                html.P(
                                    'Erforsche Deine hochgeladene Daten mithilfe unterschiedlicher interaktiver Diagramme.',
                                    className='card-text3',
                                ),
                                dbc.Row([
                                    dbc.Col(width=11),
                                    dbc.Col(dcc.Link(dbc.Button('Auswählen', color='secondary', style={'font-size' : '14px'}), href='/interaktive-diagrame'),width=1),
                                ],style={'position':'absolute', 'bottom':'0', 'left':'15px'})
                                    
                                    
                            ], className='method-body'), width=9)
                        ])
                    ], className='method-card'), width=4),
                ], style={'text-align':'left'})
            ])
        ], className='lobby-card'),

        dbc.Card([
            html.Div([
                html.H2('Freitext-Analyse'),
                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                html.P('', style={'margin-bottom': '5px'}, className='card-text1'),
            
            ], style={'margin':'20px', 'text-align':"left"}),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(dbc.Card([
                        dbc.Row([
                        dbc.Col(dbc.CardImg(src='assets/img/clustering200x150.png', top=True, style={'border-right': '1px #3c414333 solid'}),width=3),
                        dbc.Col(dbc.CardBody([
                                html.H4('Clustering-Analyse', className='card-title'),
                                html.P(
                                    'Führe für ausgewählte Freitexte eine hierarchischen Clusteranalyse mithilfe von agglomerativen Berechnungen durch. Wähle die gewünschte Cluster-Anzahl und erhalte Dashboard mit semantischen Analysen zu den erstellten Cluster.',
                                    className='card-text3',
                                ),
                                dbc.Row([
                                    dbc.Col(width=11),
                                    dbc.Col(dcc.Link(dbc.Button('Auswählen', color='secondary', style={'font-size' : '14px'}), href='/clustering'),width=1),
                                ],style={'position':'absolute', 'bottom':'0', 'left':'15px'})
                            ], className='method-body'), width=9)
                        ])
                    ], className='method-card'), width=4),
                    dbc.Col(dbc.Card([
                        dbc.Row([
                            dbc.Col(dbc.CardImg(src='assets/img/summarization200x150.png', top=True, style={'border-right': '1px #3c414333 solid'}),width=3),
                            dbc.Col(dbc.CardBody([
                                    html.H3('Text Summarizer', className='card-title'),
                                    html.P(
                                        'Lasse Dir eine Zusammenfassung der in einer ausgewählten Spalte enthaltenden Freitext ausgeben.',
                                       className='card-text3',
                                    ),
                                    dbc.Row([
                                        dbc.Col(width=11),
                                        dbc.Col(dcc.Link(dbc.Button('Auswählen', color='secondary', style={'font-size' : '14px'}), href='/summarizer'),width=1),
                                    ],style={'position':'absolute', 'bottom':'0', 'left':'15px'})
                                ], className='method-body'), width=9)
                            ])
                    ], className='method-card'), width=4),
                    dbc.Col(dbc.Card([
                        dbc.Row([
                            dbc.Col(dbc.CardImg(src='assets/img/sentiment200x150.png', top=True, style={'border-right': '1px #3c414333 solid'}),width=3),
                            dbc.Col(dbc.CardBody([
                                    html.H3('Sentiment Analyse', className='card-title'),
                                    html.P(
                                        'Lasse Dir mithilfe der Sentiment Analyse das Stimmungsbild von Freitexten einer ausgewählten Spalte ausgeben.',
                                       className='card-text3',
                                    ),
                                    dbc.Row([
                                        dbc.Col(width=11),
                                        dbc.Col(dcc.Link(dbc.Button('Auswählen', color='secondary', style={'font-size' : '14px'}), href='/sentiment'),width=1),
                                    ],style={'position':'absolute', 'bottom':'0', 'left':'15px'})
                                ], className='method-body'), width=9)
                            ])
                    ], className='method-card'), width=4),
                ]),
            ])
        ], className='lobby-card'),

        dbc.Modal([
            dbc.ModalBody(
                html.Div([
                    html.Div([html.H4('Notwendige Angabe!', style={"margin":"10px 0 30px 0"})], id='modal-headline'),
                    html.P('Für die erfolgreiche und fehlerfreie Durchführung der verschiedenen Analyseverfahren an den hochgeladenen Daten und den verschiedenen Datentypen ist es notwendig, dass Du angibst, ', className='card-text2'),
                    html.Ul([
                        html.Li('(1) welche Merkmale (Spalten) der Daten aus Freitexten bestehen ', className='card-text2'),
                        html.Li('(2) und welche Merkmale (Spalten) einen aus einer begrenzten Anzahl verschiedener fest vordefinierter (numerischen) Werte annehmen kann.', className='card-text2')
                    ], style={'margin-bottom':'0', 'padding-bottom': '0', 'font-weight': 'bold'}),
                    html.P('Du kannst erst fortfahren, wenn Du für alle Merkmale (Spalten) diese Informationen hinterlegst.', className='card-text2', style={'margin-top': '15px'}),
                    dbc.Card([
                        dbc.CardHeader(
                            dbc.Tabs(
                                [
                                    dbc.Tab(label="Angaben", tab_id="tab-1"),
                                    dbc.Tab(label="Ausschnitt der Daten", tab_id="tab-2"),
                                ],
                                id="tabs",
                                active_tab="tab-1",
                            )
                        ),
                        dbc.CardBody(
                            html.Div([
                                html.P('(1) Merkmale (Spalten), die Freitexte enthalten:', className='card-text2', style={'margin-top': '10px', 'font-weight': 'bold'}),
                                dcc.Dropdown(id='freitext-dropdown', options=[{'label':'-', 'value':'-'}], value='-', multi=True, placeholder='Füge die richtigen Merkmale (Spalten) hinzu ...', style={'margin': '0'}, className='dropdown'),
                                                        
                                html.P('(2) Merkmale (Spalten), die begrenzten Anzahl verschiedener fest vordefinierter (numerischer) Werte enthalten:', className='card-text2', style={'margin-top': '40px', 'font-weight': 'bold'}),
                                dcc.Dropdown(id='festtext-dropdown', options=[{'label':'-', 'value':'-'}], value='-', multi=True, placeholder='Füge die richtigen Merkmale (Spalten) hinzu ...', style={'margin': '0'}, className='dropdown'),
                            ]), id="content-1"
                        ),
                        dbc.CardBody(
                            html.Div([
                                html.H2('Ausschnitt der Daten: '),
                                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                                html.Div([], id='datatable')
                            ]), id="content-2"
                        )
                    ], style={'margin-top': '40px'}),
                    html.P('Wichtig: Bei falscher Zuordnung der Merkmale (Spalten) können innerhalb der verschiedenen Analyseverfahren Fehler auftreten oder die Ergebnisse nicht korrekt sein. Die deskriptive Auswertung ist lediglich von Merkmalen (Spalten) möglich, die eine begrenzte Anzahl unterschiedler Werte  enthält. Die semantischen Freitext-Analysen lassen sich lediglich auf Freitexte anwenden.', className='card-text2', style={'color': 'red', 'margin-top': '30px', 'font-weight': 'bold'}),
                ])
            ),
            dbc.ModalFooter(
                
                html.Div([
                    dbc.Button('Bestätigen', color='secondary', id='apply-btn1', style={'display': 'None'}),
                    dbc.Button('Bestätigen', color='secondary', id='apply-btn2', outline=True, style={'background': '#f2f2f2', 'color' : '#3c4143'})
                ])
            ),
        ],
        id='modal-backdrop',
        is_open=False,
        backdrop='static',
        size='xl'
    ),
                
                   
    ], id='lobby', style={'display':'block'}),

    
        
], className='content', fluid=True)

@app.callback([Output("content-1", "style"), Output("content-2", "style")], [Input("tabs", "active_tab")])
def tab_content(active_tab):
    style1 = {'display':'block'}
    style2 = {'display':'none'}

    if active_tab == 'tab-1':
        return style1, style2
    
    else: 
        return style2, style1

@app.callback([Output('datatable', 'children'),
                Output('freitext-dropdown', 'options'),
                Output('festtext-dropdown', 'options'),
                Output('apply-btn1', 'style'),
                Output('apply-btn2', 'style')],
    [Input('main_data_after_preperation', 'data'), 
    Input('freitext-dropdown', 'value'),
    Input('festtext-dropdown', 'value')],
    [State('freitext-dropdown', 'options'),
    State('festtext-dropdown', 'options')])

def update_modal(data, freitext_value, festtext_value, freitext_options, festtext_options):
    count_1=0
    count_2=0
    style1 = {'display':'block'}
    style2 = {'display':'none'}   

    if data is not None:
        freitext_options = []
        festtext_options = []
        df = pd.read_json(data, orient='split')
        df1 = df.drop(columns=[df.columns[0]])
        df2 = df1
        count_col=len(df1.columns)
        
        if freitext_value != '-':
            for col in freitext_value:
                df2 = df2.drop(columns=[col])
        if festtext_value != '-':
            for col in festtext_value:
                df1 = df1.drop(columns=[col])

        for col in df1.columns:
            freitext_options.append({'label':col, 'value': col})
        for col in df2.columns:
            festtext_options.append({'label':col, 'value': col})

        children = tablesFuncs.tableHead(df)
        
        if freitext_value != '-':
            count_1 = len(freitext_value)

        if festtext_value != '-':
            count_2 =len(festtext_value)
        
        if count_1 + count_2 == count_col:
            return children, freitext_options, festtext_options, style1, style2
    
        else:
            return children, freitext_options, festtext_options, style2, style1
    else: 
        return None, freitext_options, festtext_options, style2, style1 

    
@app.callback([Output('listOfFrei', 'data'),
                Output('listOfFest', 'data'),
                Output('cur_data', 'data')],
                [Input("apply-btn1", "n_clicks"),
                Input('freitext-dropdown', 'value'),
                Input('festtext-dropdown', 'value')],
                [State('listOfFrei', 'data'),
            State('listOfFest', 'data'),
            State('main_data_after_preperation', 'data'),
            State('cur_data', 'data')])
def update_lists(click, freitext_value, festtext_value, listOfFrei, listOfFest, data, cur_data):
    
    if data is not None:
        
        if cur_data is not None:
            df = pd.read_json(data, orient='split')
            df_cur = pd.read_json(cur_data, orient='split')
            
            if df.equals(df_cur) == False:
                cur_data = data
                listOfFrei = None
                listOfFest = None
                       
        if click:
            cur_data = data
            return freitext_value, festtext_value, cur_data
        
        else:
            return listOfFrei, listOfFest, cur_data

    else:
        return None, None, None             


@app.callback(Output("modal-backdrop", "is_open"),
            [Input("apply-btn1", "n_clicks"),
            Input('listOfFrei', 'data'),
            Input('listOfFest', 'data')],
            State('main_data_after_preperation', 'data'))
def toggle_modal(click, listOfFrei, listOfFest, data):

    if data is None:
        return False
    elif click or listOfFrei != None or listOfFest != None:
        return False
    else:
        return True


@app.callback([Output({'type':'errorView', 'index':1}, 'style'), Output('lobby', 'style')],
               [Input('main_data_after_preperation', 'data')])
def prepare_data(main_data):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    
    if main_data is None:
        return style1, style2
    
    else:
        return style2, style1