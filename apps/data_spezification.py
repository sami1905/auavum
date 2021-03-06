from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import pandas as pd
from app import app

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
    ], id={'type':'errorView', 'index':9}, className='alert-wrapper', style={'display':'none'}),
    
    # Main-content
    html.Div([
        dbc.Row([
            dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
            dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
            dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
        ] ,className='header'),

        dbc.Row([
            dbc.Col([], width=3),
            dbc.Col(html.Img(src='assets/img/progress2of4.png', className='progress-img'), width=6),
            dbc.Col(html.Div(id='output-alert-prepare', style={'display':'none'}, className='upload-alert'),width=3)
        ], className='progress-row'),

        
        dbc.Card([
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(width=1),
                    dbc.Col(html.Div([
                        html.H1('Schritt 2: Daten vorbereiten'),
                        html.P('Bereite Deine hochgeladene Daten, vor bevor Du ein Analyse-Verfahren wählst.', style={'margin-bottom': '5px'}, className='card-text1'),
                    ]),width=10),
                    dbc.Col(width=1),
                ])
            ])
        ], className='setting-card'),

        
        
        dbc.Card([
           html.Div([
                html.H2('Notwendige Angabe!'),
                html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                html.P('Für die erfolgreiche und fehlerfreie Durchführung der verschiedenen Analyseverfahren an den hochgeladenen Daten und den verschiedenen Datentypen ist es notwendig, dass Du angibst, ', className='card-text2'),
                html.Ul([
                    html.Li('(1) welche Merkmale (Spalten) der Daten aus Freitexten bestehen ', className='card-text2'),
                    html.Li('(2) und welche Merkmale (Spalten) einen aus einer begrenzten Anzahl verschiedener fest vordefinierter (numerischen) Werte annehmen kann.', className='card-text2')
                ], style={'margin-bottom':'0', 'padding-bottom': '0', 'font-weight': 'bold'}),
                html.P('Du kannst erst fortfahren, wenn Du für alle Merkmale (Spalten) diese Informationen hinterlegst.', className='card-text2', style={'margin-top': '15px'}),
                html.Div([
                    html.P('(1) Merkmale (Spalten), die Freitexte enthalten:', className='card-text2', style={'margin-top': '40px', 'font-weight': 'bold'}),
                    dcc.Dropdown(id='freitext-dropdown', options=[{'label':'-', 'value':'-'}], value='-', multi=True, placeholder='Füge die richtigen Merkmale (Spalten) hinzu ...', style={'margin': '0'}, className='dropdown'),
                                                        
                    html.P('(2) Merkmale (Spalten), die begrenzten Anzahl verschiedener fest vordefinierter (numerischer) Werte enthalten:', className='card-text2', style={'margin-top': '40px', 'font-weight': 'bold'}),
                    dcc.Dropdown(id='festtext-dropdown', options=[{'label':'-', 'value':'-'}], value='-', multi=True, placeholder='Füge die richtigen Merkmale (Spalten) hinzu ...', style={'margin': '0'}, className='dropdown'),
                ]),
                html.P('Wichtig: Bei falscher Zuordnung der Merkmale (Spalten) können innerhalb der verschiedenen Analyseverfahren Fehler auftreten oder die Ergebnisse nicht korrekt sein. Die deskriptive Auswertung ist lediglich von Merkmalen (Spalten) möglich, die eine begrenzte Anzahl unterschiedler Werte  enthält. Die semantischen Freitext-Analysen lassen sich lediglich auf Freitexte anwenden.', className='card-text2', style={'color': 'red', 'margin-top': '30px', 'font-weight': 'bold', 'font-size':'16px'}),
                dbc.Row([
                    dbc.Col(dcc.Link(dbc.Button('Zurück', color='secondary', style={'textAlign': 'center'}), href='/daten-vorbereiten'), width=1),
                    dbc.Col(width=10),
                    dbc.Col([dcc.Link(dbc.Button('Weiter', color='secondary', style={'textAlign': 'center'}, id='apply-btn1', n_clicks=0), href='/verfahren-waehlen'), 
                    dbc.Button('Weiter', color='secondary', id='apply-btn2', outline=True, style={'background': '#f2f2f2', 'color' : '#3c4143'})], width=1),
                ], style={'text-align':'center', 'margin':'40px 0px 0px 0px'})
            ], style={'text-align':'left', 'padding':'30px'})
                        
        ], className='setting-card'),
        dbc.Card([
           html.Div(id='spezification-table', style={'text-align':'left', 'padding':'30px'})
                        
        ], className='data-card')  
    ], id='data-spezification', style={'display':'none'}),
], className='content', fluid=True)

@app.callback(Output('spezification-table', 'children'),
        [Input('main_data_after_preperation', 'data')])
def show_table(data):
    if data is not None:
        df = pd.read_json(data, orient='split')
        
                          
        children_table = [
            html.H2('Daten', style={'margin': '20px 0 5px 0', 'padding':'0'}),
            html.Hr(style={'margin': '0 0 20px 0', 'padding':'0'}),
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)
        ]
        
        return children_table
    
    else: return None



@app.callback([Output({'type':'errorView', 'index':9}, 'style'), Output('data-spezification', 'style')],
               [Input('main_data_after_preperation', 'data')])
def error(main_data):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    
    
    if main_data is None:
        return style1, style2
    
    else:
        return style2, style1



@app.callback([Output('freitext-dropdown', 'options'),
                Output('festtext-dropdown', 'options'),
                Output('apply-btn1', 'style'),
                Output('apply-btn2', 'style')],
    [Input('main_data_after_preperation', 'data'), 
    Input('freitext-dropdown', 'value'),
    Input('festtext-dropdown', 'value')],
    [State('freitext-dropdown', 'options'),
    State('festtext-dropdown', 'options')])

def update_modal(data, freitext_value, festtext_value, freitext_options, festtext_options):
    style1 = {'display':'block'}
    style2 = {'display':'none'}   
    count_1 = 0
    count_2 = 0
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


        
        if freitext_value != '-':
            count_1 = len(freitext_value)

        if festtext_value != '-':
            count_2 =len(festtext_value)
        
        if count_1 + count_2 == count_col:
            return freitext_options, festtext_options, style1, style2
    
        else:
            return freitext_options, festtext_options, style2, style1
    else: 
        return freitext_options, festtext_options, style2, style1 

    
@app.callback([Output('listOfFrei', 'data'),
                Output('listOfFest', 'data')],
                [Input("apply-btn1", "n_clicks"),
                Input('freitext-dropdown', 'value'),
                Input('festtext-dropdown', 'value')],
                [State('listOfFrei', 'data'),
            State('listOfFest', 'data'),
            State('main_data_after_preperation', 'data')])
def update_lists(click, freitext_value, festtext_value, listOfFrei, listOfFest, data, ):
    listOfFrei = None
    listOfFest = None
    if click:
        return freitext_value, festtext_value
        
    else:
        return listOfFrei, listOfFest

    
 