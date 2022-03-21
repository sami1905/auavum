import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import pandas as pd
from app import app
import functions.getTable as tablesFuncs


layout = dbc.Container([
    
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
    ],  id={'type':'errorView', 'index':1}, className='alert-wrapper', style={'display':'none'}),
    
    # Main-content
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
            dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
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
                    dbc.Col(dcc.Link(dbc.Button('Zurück', color='secondary', style={'position' : 'relative', 'left': '-25px'}), href='/daten-spezifizieren'),width=1),
                    dbc.Col(html.Div([
                        html.H1('Schritt 3: Verfahren wählen'),
                        html.P('Wähle ein Verfahren mit dem die Auswertung und Analyse durchgeführt werden soll.', style={'margin-bottom': '5px'}, className='card-text1')
                    ]),width=10),
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
                   
    ], id='lobby', style={'display':'block'}),

    
        
], className='content', fluid=True)



           
@app.callback([Output({'type':'errorView', 'index':1}, 'style'), Output('lobby', 'style')],
               [Input('main_data_after_preperation', 'data'), Input('listOfFrei', 'data'),
                Input('listOfFest', 'data')])
def error(main_data, d1, d2):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    
    if main_data is None or d1 is None or d2 is None:
        return style1, style2
    
    else:
        return style2, style1