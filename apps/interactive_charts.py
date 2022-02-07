from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.express as px
from app import app
import dash
import json


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
    ],  id={'type':'errorView', 'index':3}, className='alert-wrapper', style={'display':'none'}),
    
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
                    dbc.Col(dcc.Link(dbc.Button("Zurück", color="secondary", style={'position' : 'relative', 'left': '-25px'}), href="/verfahren-waehlen"),width=1),
                    dbc.Col(html.Div([
                        html.H1('Schritt 4: Ergebnis erhalten'),
                        html.P('Erstelle Dein eigenes Diagramm-Dashboard zu Deinen hochgeladenen Daten.', style={'margin-bottom': '5px'}, className='card-text1')
                    ]),width=10),
                    dbc.Col(width=1),
                ])
            ])
        ], className='deskriptiv-card'),
        
        dbc.Card([
            
                dbc.Tabs(
                    [
                        dbc.Tab(label="Interaktive Diagramme", tab_id="tab-1"),
                        dbc.Tab(label="Daten", tab_id="tab-2"),
                    ],
                    id="card-tabs",
                    active_tab="tab-1",
                    style={'background': '#f2f2f263'}
                ),
            dbc.CardBody([
                    html.H4("Interaktive Diagramme"),
                    html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
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
                                ]),
                                width=2),
                            dbc.Col(
                                html.Div([
                                    html.P('Ebenen:', className='card-text2', style={'margin': '5px 0 0 10px'}),
                                    dbc.Row([
                                        html.Div([
                                            dbc.Row([
                                                # dcc.Dropdown(id='layer1', 
                                                #             options=[{'label': 'Neuen Index hinzufügen', 'value': 'new'}], 
                                                #             value='new', 
                                                #             clearable=False,
                                                #             searchable=False,
                                                #             className='dropdown',
                                                #             style={'font-size': '14px', 'width': '300px'}),
                                                # dcc.Dropdown(id='layer2', 
                                                #             options=[{'label': 'Neuen Index hinzufügen', 'value': 'new'}], 
                                                #             value='new', 
                                                #             clearable=False,
                                                #             searchable=False,
                                                #             className='dropdown',
                                                #             style={'font-size': '14px', 'width': '300px'}),
                                                # dcc.Dropdown(id='layer3', 
                                                #             options=[{'label': 'Neuen Index hinzufügen', 'value': 'new'}], 
                                                #             value='new', 
                                                #             clearable=False,
                                                #             searchable=False,
                                                #             className='dropdown',
                                                #             style={'font-size': '14px', 'width': '300px'})
                                            ], id='layer-list'),
                                        ], style={'margin': '0 30px'}),
                                        dbc.Button([html.Img(src='/assets/img/plus_icon32x25.png', width='32px', height='25px'),"Ebene hinzufügen"], style={'margin' : '10px', 'display': 'None'}, color="success", id="new_layer1", n_clicks=3),
                                        dbc.Button([html.Img(src='/assets/img/plus_icon32x25_dark.png', width='32px', height='25px'),"Ebene hinzufügen"], color='secondary', id="new_layer2", outline=True, style={'display': 'None', 'background': '#f2f2f2', 'color' : '#3c4143', 'margin' : '10px'}),
                                        dbc.Button([html.Img(src='/assets/img/delete_icon14x17.png', height='17px'),"   | Ebene entfernen"], style={'margin' : '10px', 'display': 'None'}, color="danger", id="delete_layer1", n_clicks=0),
                                        dbc.Button([html.Img(src='/assets/img/delete_icon17x20.png', height='17px'),"   | Ebene entfernen"], color='secondary', id="delete_layer2", outline=True, style={'display': 'None', 'background': '#f2f2f2', 'color' : '#3c4143', 'margin' : '10px'})
                                        
                                    ])
                                ]),width=10)
                        ]),
                    ]),
                    html.Div([
                        html.P('Diagramm' , className='card-text2', style={'font-weight': 'bold', 'margin-top':'30px'}),
                        html.Div([
                            dcc.Graph(id='interactive-figure', figure = {})
                            ], style={'text-align':'center', 'margin':'0 auto'})
                    ]),        
            ], id="tab_figure", style={'text-align': 'left'}),
            
            dbc.CardBody([
                html.H4("Daten", style={'text-align': 'left'}),
                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                html.Div(id='show-interactive-data')
            ], id="tab_datatable")
        ], className='interactive-card')
    ], id="interactive-charts"),
], className='content', fluid=True)


@app.callback(Output('show-interactive-data', 'children'), Input('main_data_after_preperation', 'data'))
def show_data(data):
    if data is not None:
        df = pd.read_json(data, orient='split')
        df = df.fillna('Keine Angaben')
        children = [html.Div([dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)], style={'text-align': 'left'})]

        return children
    return None

@app.callback(
    [Output("tab_figure", "style"), Output("tab_datatable", "style")], [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    style1 = {'display':'block'}
    style2 = {'display':'none'}

    if active_tab == 'tab-1':
        return style1, style2
    
    else: 
        return style2, style1

# @app.callback([Output('layer1', 'options'), Output('layer1', 'value'),
#                 Output('layer2', 'options'), Output('layer2', 'value'),
#                 Output('layer3', 'options'), Output('layer3', 'value')],
#                 [Input('listOfFest', 'data'), Input('layer1', 'value'), Input('layer2', 'value'), Input('layer3', 'value')])
# def update_dropdowns(listOfFest, value1, value2, value3):
#     listOfFest1 = listOfFest.copy()
#     listOfFest2 = listOfFest.copy()
#     listOfFest3 = listOfFest.copy()

#     options1 = []
#     options2 = []
#     options3 = []
    
    
#     if value1 == 'new' or value2 == 'new' or value3 == 'new':
#         value1 = listOfFest[0]
#         value2 = listOfFest[1]
#         value3 = listOfFest[2]

    
#     listOfFest2.remove(value1)
#     listOfFest3.remove(value1)
   
#     listOfFest1.remove(value2)
#     listOfFest3.remove(value2)
    
#     listOfFest1.remove(value3)
#     listOfFest2.remove(value3)

#     for col in listOfFest1:
#         options1.append({'label':col, 'value': col})
#     for col in listOfFest2:
#         options2.append({'label':col, 'value': col})
#     for col in listOfFest3:
#         options3.append({'label':col, 'value': col})

#     return options1, value1, options2, value2, options3, value3


@app.callback(
    [Output('layer-list', 'children'),
    Output('delete_layer1', 'n_clicks')],
    [Input('new_layer1', 'n_clicks'),
    Input('delete_layer1', 'n_clicks')],
    [State('layer-list', 'children'),
    State('listOfFest', 'data')])
def display_dropdowns(new_layer, delete_layer, children, listOfFest):
    options = []
    if listOfFest is not None:
        for col in listOfFest:
            options.append({'label':col, 'value': col})
        
        
        if new_layer == 3 and not delete_layer:
            new_dropdown = dcc.Dropdown(
                id={'type': 'filter-dropdown','index': 0},
                options=options, 
                value=listOfFest[0], 
                clearable=False,
                searchable=False,
                className='dropdown',
                style={'font-size': '14px', 'width': '300px'})
            
            children.append(new_dropdown)
            new_dropdown = dcc.Dropdown(
                id={'type': 'filter-dropdown','index': 1},
                options=options, 
                value=listOfFest[1], 
                clearable=False,
                searchable=False,
                className='dropdown',
                style={'font-size': '14px', 'width': '300px'})
            children.append(new_dropdown)
            new_dropdown = dcc.Dropdown(
                id={'type': 'filter-dropdown','index': 2},
                options=options, 
                value=listOfFest[2], 
                clearable=False,
                searchable=False,
                className='dropdown',
                style={'font-size': '14px', 'width': '300px'})
            children.append(new_dropdown)
        
        elif new_layer > 3 and not delete_layer:
            new_dropdown = dcc.Dropdown(
                id={'type': 'filter-dropdown','index': new_layer-1},
                options=options, 
                value=listOfFest[new_layer-1], 
                clearable=False,
                searchable=False,
                className='dropdown',
                style={'font-size': '14px', 'width': '300px'})
            children.append(new_dropdown)
        
        
        elif len(children) > 3 and delete_layer:
            children = children[:-1]

    return children, 0



    
@app.callback(
    [Output('new_layer1', 'style'),
    Output('delete_layer1', 'style'),
    Output('new_layer2', 'style'),
    Output('delete_layer2', 'style')],
    [Input('layer-list', 'children')],
    [State('listOfFest', 'data')])
def display_dropdowns(layerList, listOfFest): 
    style1 = {'margin': '0 0 0 10px', 'display':'block'}
    style2 = {'display':'none'}

    if listOfFest is not None:
        if len(layerList) == len(listOfFest):
            return style2, style1, style1, style2

        if len(layerList) == 3:
            return style1, style2, style2, style1

        else:
            return style1, style1, style2, style2
    else:
        return style1, style1, style2, style2     

@app.callback(
    Output('interactive-figure', 'figure'),
    [Input({'type': 'filter-dropdown', 'index': ALL}, 'value'),
    Input('chart-type', 'value')],
    [State('main_data_after_preperation', 'data')]
)
def get_figur(values, chart_type, data):
    listofCols = []
    fig = {}
    if data is not None:
        for (i, value) in enumerate(values):
            listofCols.append(value)
        
        df = pd.read_json(data, orient='split')
        df = df.fillna('Keine Angaben')
        df = df[listofCols]

        if chart_type == 1:
            fig = px.sunburst(df, path=listofCols, width=1200, height=1200)
        elif chart_type == 2:
            fig = px.icicle(df, path=listofCols, width=1600, height=1200)
        elif chart_type == 3:
            fig = px.treemap(df, path=listofCols, width=1600, height=1200)
        elif chart_type == 4:
            fig = px.parallel_categories(df, width=1600, height=1200)

    return fig

@app.callback([Output({'type':'errorView', 'index':3}, 'style'), Output('interactive-charts', 'style')],
               [Input('main_data_after_preperation', 'data'),
               Input('listOfFest', 'data'),
               Input('listOfFrei', 'data')])
def error3(main_data, d1, d2):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    
    if main_data is None or d1 is None or d2 is None:
        return style1, style2
    
    else:
        return style2, style1

