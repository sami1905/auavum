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
    ],  id={'type':'errorView', 'index':2}, className='alert-wrapper', style={'display':'none'}),
    
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
                        dbc.Tab(label="Diagramm-Dashboard", tab_id="tab-1"),
                        dbc.Tab(label="Daten", tab_id="tab-2"),
                    ],
                    id="card-tabs",
                    active_tab="tab-1",
                    style={'background': '#f2f2f263'}
                ),
            dbc.CardBody([
                    
                    
                    html.H4("Diagramm-Dashboard", style={'text-align': 'left'}),
                    html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                    dbc.Row([
                        dbc.Col(width=10),
                        dbc.Col(
                            dbc.Row([
                                dbc.Button([html.Img(src='/assets/img/plus_icon32x25.png', width='32px', height='25px'),"Diagramm hinzufügen"], style={'margin' : '0 10px 0 0'}, color="success", id="new_graph", n_clicks=0),
                                #dbc.Button(html.Img(src='/assets/img/dowload_icon15x15.png', width='15px', height='15px'), color="dark")
                            ],  style={'float' : 'right', 'margin-right': '3px'}),width=2)
                    ]),
                    html.Div([
                        dbc.Row([],id='figures',  className='figures')
                    ]),
                    
            ],id="tab_figures"),
            
            dbc.CardBody([
                html.H4("Daten", style={'text-align': 'left'}),
                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                html.Div(id='show-deskriptiv-data')
            ], id="tab_data")
        ], className='deskriptiv-card')
    ], id="deskriptiv"),
], className='content', fluid=True)

@app.callback(Output('figures', 'children'),
            [Input('main_data_after_preperation', 'data'), 
            Input('new_graph', 'n_clicks'),
            Input({'type':'dynamic-delete-btn', 'index': ALL}, 'n_clicks'),
            Input('listOfFrei', 'data')],
            [State('figures', 'children')])
def update_listOfFigures(data, clicks, _,listOfFrei, div_children):
    
    input_value=""
    input_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if "index" in input_id:
        delete_chart = json.loads(input_id)["index"]
        div_children = [
            chart
            for chart in div_children
            if "'index': " + str(delete_chart) not in str(chart)
        ]

    else:
        if clicks != 0:
            histo_x_option=[]
            histo_y_option=[{'label':'Anzahl', 'value':'Anzahl'}]
            histo_group_option=[{'label':'-', 'value':'-'}]
            pie_option=[]
            if data is not None:
                df = pd.read_json(data, orient='split')
                df = df.fillna('Keine Angaben')
                
                df = df.set_index(df.columns[0])
                if listOfFrei != None:
                    for col in listOfFrei:
                        df = df.drop(columns=[col])
                
                i=0
                for col in df.columns:
                
                    histo_x_option.append({'label':col, 'value':df.columns.get_loc(col)})
                    histo_y_option.append({'label':col, 'value':df.columns.get_loc(col)})
                    histo_group_option.append({'label':col, 'value':df.columns.get_loc(col)})
                    pie_option.append({'label':col, 'value':df.columns.get_loc(col)})
                    if i == 0:
                        histo_value=df.columns.get_loc(col)
                        pie_value=df.columns.get_loc(col)
                        input_value = col
                    i=i+1
                fig = px.histogram(df, x=df.columns[0])
                fig.update_layout(title ="Diagramm: " + str(clicks), yaxis_title='Anzahl')            
                children=dbc.Col(html.Div([
                    html.Div([
                        html.Div([html.H1("Diagramm: " + str(clicks), style={'margin':'2px 0 0 0'})], id={'type':'dynamic-headline-chart', 'index': clicks}),
                        
                    ], style={'background': '#f2f2f2', 'padding':'4px'}),
                    
                    dbc.Row([
                        dbc.Button(html.Img(src='/assets/img/edit_icon14x18.png', style={'margin' : '-13px 0 0 -6px'}), style={'margin' : '0 5px 0 0', 'border-radius': '50px', 'width':'28px', 'height':'28px'}, color="warning", n_clicks=0, id={'type':'dynamic-prepare-btn', 'index': clicks}),
                        dbc.Button(html.Img(src='/assets/img/delete_icon14x17.png',  style={'margin' : '-13px 0 0 -6px'}), style={'border-radius': '50px', 'width':'28px', 'height':'28px'}, color="danger", n_clicks=0, id={'type':'dynamic-delete-btn', 'index': clicks})
                    ], style={'float' : 'right', 'margin': '7px 3px'}),    
                    dcc.Graph(id={'type':'dynamic-graph', 'index': clicks}, figure = fig, style={'margin-top' : '40px'}),
                    html.Div([], id={'type':'dynamic-chart-description', 'index': clicks}, style={'text-align' : 'left'}),                  
                    dbc.Modal([
                        
                        dbc.ModalBody(
                            html.Div([
                                html.Div([html.H4("Diagramm: " + str(clicks), style={"margin":"10px 0 30px 0"})], id={'type':'dynamic-pre-headline-chart', 'index': clicks}),
                                    html.P("Vorschau:" , className="card-text2", style={"font-weight": "bold", "margin":"30px 0 0 0"}),
                                        
                                    dcc.Graph(id={'type':'dynamic-pre-graph', 'index': clicks}, figure = {}),
                                    
                                    html.Div([
                                        html.P("Wähle die Art des Diagramms:" , className="card-text2", style={"font-weight": "bold"}),
                                        dcc.Dropdown(id={'type':'dynamic-chart-type', 'index': clicks}, options= [{'label':'Histogramm', 'value':1},
                                                                                    {'label':'Balkendiagramm', 'value':2},
                                                                                    {'label':'Kreisdiagramm', 'value':3},], value=1, searchable=False, clearable=False, className='dropdown')
                                    ]),
                                    
                                    html.Div([
                                        html.P("Wähle das Merkmal für die X-Achse:" , className="card-text2", style={"font-weight": "bold", "margin":"15px 0 0 0"}),
                                        html.P("Beachte: Wähle für die Werte der X-Achse lediglich Merkmale aus geschlossenen Fragen - KEINE Freitextantworten!" , className="card-text2"),
                                        dcc.Dropdown(id={'type':'dynamic-histo-x', 'index': clicks}, options= histo_x_option, value=histo_value, searchable=False, clearable=False, className='dropdown'),
                                        
                                        html.P("Wähle das Merkmal für die Y-Achse:" , className="card-text2", style={"font-weight": "bold", "margin":"15px 0 0 0"}),
                                        html.P("Beachte: Die Y-Achse muss numerische Werte enthalten. Die Auswahl von Text-Attributen kann zu Fehler führen!" , className="card-text2"),
                                        dcc.Dropdown(id={'type':'dynamic-histo-y', 'index': clicks}, options= histo_y_option, value='Anzahl', searchable=False, clearable=False, className='dropdown'),
                                        
                                        html.P("Wenn die Attribute der X-Achse gruppiert werden sollen, wähle das Merkmal:" , className="card-text2", style={"font-weight": "bold", "margin":"15px 0 0 0"}),
                                        dcc.Dropdown(id={'type':'dynamic-histo-group', 'index': clicks}, options=histo_group_option, value='-', searchable=False, clearable=False, className='dropdown'),

                                    ], id={'type':'dynamic-bar-setttings', 'index': clicks}),
                                    
                                    html.Div([
                                        html.P("Wähle das Merkmal, das als Kreisdiagramm dargestellt werden soll:" , className="card-text2", style={"font-weight": "bold", "margin":"15px 0 0 0"}),
                                        dcc.Dropdown(id={'type':'dynamic-pie-col', 'index': clicks}, options= pie_option, value=pie_value, searchable=False, clearable=False, className='dropdown'),
                                    ], id={'type':'dynamic-pie-setttings', 'index': clicks}, style={"display":'none'}),
                                    html.Div([
                                        html.P("Beschriftung:" , className="card-text2", style={"font-weight": "bold", "margin":"15px 0 0 0"}),
                                        dbc.Row([
                                            html.P("Überschrift: " , className="card-text2"),
                                            dbc.Input(id={'type':'dynamic-chart-titel', 'index': clicks}, value='Diagramm: ' + str(clicks), type='text', placeholder='Füge einen Titel für das Diagramm hinzu...'),
                                        ], style={"margin":'5px 1px'}),
                                            
                                    ], id={'type':'dynamic-chart-label', 'index': clicks}, style={"display":'block'}),
                                    html.Div([
                                        dbc.Row([
                                            html.P("X-Achse: " , className="card-text2"),
                                            dbc.Input(id={'type':'dynamic-chart-x', 'index': clicks}, value=input_value, type='text', placeholder='Beschrifte die X-Achse...'),
                                        ], style={"margin":'5px 1px'}),
                                        dbc.Row([
                                            html.P("Y-Achse: " , className="card-text2"),
                                            dbc.Input(id={'type':'dynamic-chart-y', 'index': clicks}, value='Anzahl', type='text', placeholder='Beschrifte die Y-Achse...'),
                                        ], style={"margin":'5px 1px'}),
                                            
                                    ], id={'type':'dynamic-chart-axis-label', 'index': clicks}, style={"display":'block'}),

                                    html.Div([
                                        dbc.Row([
                                            html.P("Beschreibung: " , className="card-text2"),
                                            dbc.Textarea(id={'type':'dynamic-chart-description-in', 'index': clicks}, placeholder='Füge einen Beschreibung für das Diagramm hinzu...'),
                                        ], style={"margin":'5px 1px'}),
                                    ]),
                            ])
                        ),
                        dbc.ModalFooter(
                            dbc.Row([
                                dbc.Button(
                                    "Änderung anwenden", id={'type':'dynamic-add-graph', 'index': clicks}, color="secondary", n_clicks=0
                                ),
                                dbc.Button("Abbrechen", id={'type':'dynamic-add-graph-close', 'index': clicks}, color="secondary", n_clicks=0, outline=True, 
                                                    style={'background': '#f2f2f2',
                                                        'color' : '#3c4143',
                                                        'textAlign': 'center',
                                                        'margin-left': '10px'
                                                        })
                            ]), style={'margin': '20px 0 0 0 '}
                        )
                    ], id={'type':'dynamic-graph-modal', 'index': clicks}, is_open=False, size="lg")
                
                ], style={'text-align':'center', 'border': '2px #f2f2f2 solid','border-radius': '5px', 'margin':'20px 0px 10px 0px'}), width=6)

                div_children.append(children)
            
    return div_children 

@app.callback(Output('show-deskriptiv-data', 'children'), Input('main_data_after_preperation', 'data'))
def show_data(data):
    if data is not None:
        df = pd.read_json(data, orient='split')
        df = df.fillna('Keine Angaben')
        children = [html.Div([dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)], style={'text-align': 'left'})]

        return children
    return None

@app.callback(
    [Output("tab_figures", "style"), Output("tab_data", "style")], [Input("card-tabs", "active_tab")]
)
def tab_content(active_tab):
    style1 = {'display':'block'}
    style2 = {'display':'none'}

    if active_tab == 'tab-1':
        return style1, style2
    
    else: 
        return style2, style1

@app.callback([Output({'type':'dynamic-bar-setttings', 'index': MATCH}, 'style'), 
                Output({'type':'dynamic-pie-setttings', 'index': MATCH}, 'style'),
                Output({'type':'dynamic-chart-axis-label', 'index': MATCH}, 'style')],
    [Input({'type':'dynamic-chart-type', 'index': MATCH}, 'value')])
def choose_modal_settings(value):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    if value == 1:
        return style1, style2, style1
    if value == 2:
        return style1, style2, style1
    if value == 3:
        return style2, style1, style2

@app.callback([Output({'type':'dynamic-chart-x', 'index': MATCH}, 'value'),
                Output({'type':'dynamic-chart-y', 'index': MATCH}, 'value')],
                Input({'type':'dynamic-histo-x', 'index': MATCH}, 'value'),
                Input({'type':'dynamic-histo-y', 'index': MATCH}, 'value'),
                State('listOfFest', 'data'), 
                State({'type':'dynamic-chart-x', 'index': MATCH}, 'value'),
                State({'type':'dynamic-chart-y', 'index': MATCH}, 'value'))
def update_desc(x_values, y_values, listOfFest, beschriftungX, beschriftungY):
    
    if listOfFest is not None:
        if y_values == 'Anzahl':
            beschriftungY = y_values
        else:
            beschriftungY = listOfFest[y_values]

        beschriftungX = listOfFest[x_values]
    
    return beschriftungX, beschriftungY




@app.callback([Output({'type':'dynamic-pre-graph', 'index': MATCH}, 'figure'),
                Output({'type':'dynamic-graph', 'index': MATCH}, 'figure'),
                Output({'type':'dynamic-graph-modal', 'index': MATCH}, 'is_open'), 
                Output({'type':'dynamic-add-graph', 'index': MATCH}, 'n_clicks'), 
                Output({'type':'dynamic-add-graph-close', 'index': MATCH}, 'n_clicks'),
                Output({'type':'dynamic-prepare-btn', 'index': MATCH}, 'n_clicks'),
                Output({'type':'dynamic-headline-chart', 'index': MATCH}, 'children'),
                Output({'type':'dynamic-pre-headline-chart', 'index': MATCH}, 'children'),
                Output({'type':'dynamic-chart-description', 'index': MATCH}, 'children')],
    [Input ({'type':'dynamic-chart-type', 'index': MATCH}, 'value'),
    Input({'type':'dynamic-histo-x', 'index': MATCH}, 'value'),
    Input({'type':'dynamic-histo-y', 'index': MATCH}, 'value'),
    Input({'type':'dynamic-histo-group', 'index': MATCH}, 'value'),
    Input({'type':'dynamic-pie-col', 'index': MATCH}, 'value'),
    Input('main_data_after_preperation', 'data'),
    Input({'type':'dynamic-add-graph', 'index': MATCH}, 'n_clicks'), 
    Input({'type':'dynamic-add-graph-close', 'index': MATCH}, 'n_clicks'),
    Input({'type':'dynamic-prepare-btn', 'index': MATCH}, 'n_clicks'),
    Input({'type':'dynamic-chart-titel', 'index': MATCH}, 'value'),
    Input({'type':'dynamic-chart-x', 'index': MATCH}, 'value'),
    Input({'type':'dynamic-chart-y', 'index': MATCH}, 'value')],
    [State({'type':'dynamic-graph', 'index': MATCH}, 'figure'),
    State({'type':'dynamic-headline-chart', 'index': MATCH}, 'children'),
    State({'type':'dynamic-chart-description-in', 'index': MATCH}, 'value'),
    State({'type':'dynamic-chart-description', 'index': MATCH}, 'children'),
    State('listOfFrei', 'data')],
)
def update_graphs(chart_type, x_values, y_values, groub_by, pie_col, data, n1, n2, n3, fig_title, x_title, y_title, cur_fig, headliner, description, cur_description, listOfFrei):
    df = pd.read_json(data, orient='split')
    df = df.fillna('Keine Angaben')
    
    df = df.set_index(df.columns[0])
    if listOfFrei != None:
        for col in listOfFrei:
            df = df.drop(columns=[col])
    fig = {}
    cur_headliner = headliner
    preheadliner = headliner

    if description is None or description == "":
        chart_description = None
        
    else:
        chart_description = html.Div([html.P('Beschreibung: ', className="card-text2", style={"font-weight": "bold", "margin":"30px 0 0 0"}),
                            html.P(description , className="card-text2")], style={"margin": "0 40px"})
                                        


    if chart_type == 1:
        fig= getHisto(x_values, y_values, groub_by, df)
        if y_title is not None or x_title is not None:
            fig.update_layout(
                xaxis_title=x_title,
                yaxis_title=y_title)
    if chart_type == 2: 
        fig= getBar(x_values, y_values, groub_by, df)
        if y_title is not None or x_title is not None:
            fig.update_layout(
                xaxis_title=x_title,
                yaxis_title=y_title)
    if chart_type == 3:
        fig= getPie(pie_col, df)
    
    if fig_title is not None:
        
        fig.update_layout(title=fig_title)
        headliner = [html.H1(fig_title, style={'margin':'2px 0 0 0'})]
        preheadliner = [html.H4(fig_title, style={"margin":"10px 0 30px 0"})]
    
    if n1:
        return fig, fig, False, 0, 0, 0, headliner, preheadliner, chart_description
    if n2:
        return fig, cur_fig, False, 0, 0, 0, cur_headliner, cur_headliner, cur_description

    if n3:
        return fig, cur_fig, True, n1, n2, n3, cur_headliner, preheadliner, cur_description

    else: return fig, cur_fig, False, n1, n2, n3, cur_headliner, preheadliner, cur_description


def getHisto(x_values, y_values, groupby, data):
    fig={}
    
    if y_values == 'Anzahl' and groupby != "-":
        fig = px.histogram(data, x=data.columns[x_values], color=data.columns[groupby], labels={"count":"Anzahl"}, barmode='group')
    
    if y_values != 'Anzahl' and groupby != "-":
        fig = px.histogram(data, x=data.columns[x_values], y = data.columns[y_values], color=data.columns[groupby], barmode='group')
    
    if y_values == 'Anzahl' and groupby == "-":
        fig = px.histogram(data, x=data.columns[x_values], labels={"count":"Anzahl"})
    
    if y_values != 'Anzahl' and groupby == "-":
        fig = px.histogram(data, x=data.columns[x_values], y = data.columns[y_values])
        
    return fig

def getBar(x_values, y_values, groupby, data):
    fig={}
    if y_values == 'Anzahl' and groupby != "-":
        fig = px.bar(data, x=data.columns[x_values], color=data.columns[groupby], labels={"counts":"Anzahl"}, barmode='group')
    
    if y_values != 'Anzahl' and groupby != "-":
        fig = px.bar(data, x=data.columns[x_values], y = data.columns[y_values], color=data.columns[groupby], barmode='group')
    
    if y_values == 'Anzahl' and groupby == "-":
        fig = px.bar(data, x=data.columns[x_values], labels={"counts":"Anzahl"}, barmode='group')
    
    if y_values != 'Anzahl' and groupby == "-":
        fig = px.bar(data, x=data.columns[x_values], y = data.columns[y_values], barmode='group')
        
    return fig


def getPie(col, data):
    fig = px.pie(data_frame=data, names=data.columns[col])
    return fig



@app.callback([Output({'type':'errorView', 'index':2}, 'style'), Output('deskriptiv', 'style')],
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

