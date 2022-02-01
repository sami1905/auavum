from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from app import app

layout = dbc.Container([
    dcc.Store(id='prepared_data', storage_type='local'),

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
    ], id={'type':'errorView', 'index':0}, className='alert-wrapper', style={'display':'none'}),
    
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
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(html.Div(id='get-data-informations'),width=4),
                    dbc.Col(
                        html.Div([
                            html.H2('Einstellungen'),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                           
                            
                           html.Div([
                                html.P('Wähle den Index:' , className='card-text2', style={'font-weight': 'bold'}),
                                dcc.Dropdown(id='index-dropdown', 
                                    	    options=[{'label': 'Neuen Index hinzufügen', 'value': 'new'}], 
                                            value='new', 
                                            clearable=False,
                                            searchable=False,
                                            className='dropdown')
                            ]), 
                            html.Div([
                                html.P('Wähle Spalten, die entfernt werden sollen:' , className='card-text2', style={'font-weight': 'bold', 'margin-top':'10px'}),
                                html.P('Leere Spalten', className='card-text2', style={'margin-left': '10px'}),
                                dbc.Row([
                                    dcc.Checklist(id='empty-col-check', 
                                                options=[{'label': '   ', 'value': 1}],
                                                value=[],
                                                className='checklist',
                                                style={'margin-left': '35px'}
                                                ),
                                    html.P('entfernen', className='card-text2', style={'margin-left': '10px'})
                                ]),
                                html.P('Einzelne Spalten entfernen', className='card-text2', style={'margin': '10px 0px 0px 10px'}),
                                dcc.Dropdown(id='drop-col-dropdown', options= [{'label':'-', 'value':'-'}], value=None, multi=True, placeholder='Wähle oder suche Spalten, die entfernt werden sollen...', className='dropdown')
                            ]),
                            html.Div([
                                html.P('Wähle Zeilen, die entfernt werden sollen:' , className='card-text2', style={'font-weight': 'bold', 'margin-top':'10px'}),
                                html.P('Leere Zeilen', className='card-text2', style={'margin-left': '10px'}),
                                dbc.Row([
                                    dcc.Checklist(id='empty-row-check', 
                                                options=[{'label': '   ', 'value': 1}],
                                                value=[],
                                                className='checklist',
                                                style={'margin-left': '35px'}
                                                ),
                                    html.P('entfernen', className='card-text2', style={'margin-left': '10px'})
                                ]),
                                html.P('Einzelne Zeilen' , className='card-text2', style={'margin': '10px 0px 0px 10px'}),
                                dcc.Dropdown(id='drop-row-dropdown', options= [{'label':'-', 'value':'-'}], value=None, multi=True, placeholder='Wähle den Index-Wert der Zeile(n), die entfernt werden sollen...', style={'margin': '0'}, className='dropdown'),
                            ])
                        
                        ],  style={'padding-left':'30px', 'border-left': '1px #3c414333 solid'}, className='settings'), width=8),
                ], className='data-preparation'),
                dbc.Row([
                    dbc.Col(dcc.Link(dbc.Button('Zurück', color='secondary', style={'textAlign': 'center'}), href='/'), width=1),
                    dbc.Col(width=10),
                    dbc.Col(dcc.Link(dbc.Button('Weiter', color='secondary', style={'textAlign': 'center'}, id='next-btn', n_clicks=0), href='/verfahren-waehlen'), width=1),
                ]), 
                
            ])                
        ], className='setting-card'),    
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H2('Daten'),
                             html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                        ], style={'text-align':'left'}),
                        html.Div(id='get-data'),
                            
                    ])    
                ], className='data-card'),
                
                   
    ], id='data-preparation', style={'display':'none'}),
        
], className='content', fluid=True)


@app.callback(Output('index-dropdown', 'options'),
                [Input('main_data', 'data'), Input('drop-col-dropdown', 'value')],
                [State('index-dropdown', 'options')])
def update_index(main_data, list_drop_col, options):
    
    if main_data is not None:
        options=[{'label': 'Neuen Index hinzufügen', 'value': 'new'}]
        df = pd.read_json(main_data, orient='split')
        for col in df.columns:
            if pd.Series(df[col]).is_unique:
                if list_drop_col is not None and col not in list_drop_col:
                    options.append({'label':'{}'.format(col, col), 'value':col})
                elif list_drop_col is None:
                    options.append({'label':'{}'.format(col, col), 'value':col})
    return options

@app.callback(Output('drop-col-dropdown', 'options'),
              [Input('main_data', 'data'), Input('index-dropdown', 'value'), Input('empty-col-check', 'value')],
                [State('drop-col-dropdown', 'options')])
def update_col_drop(main_data, choosen_index, drop_empty_col, options):
    if main_data is not None:
        df = pd.read_json(main_data, orient='split')
        if drop_empty_col == [1]:
            for col, col_count in zip(df.columns, df.isnull().sum()):
                if round((col_count/df.index.size)*100) == 100:
                    df=df.drop(columns=col)
        options=[]
        for col in df.columns:
            if col != choosen_index:
                options.append({'label':'{}'.format(col, col), 'value':col})
    return options

@app.callback(Output('drop-row-dropdown', 'options'),
            [Input('main_data', 'data'), Input('index-dropdown', 'value'), Input('empty-row-check', 'value')],
            [State('drop-row-dropdown', 'options')])
def update_row_drop(main_data, choosen_index, drop_empty_row, options):
    if main_data is not None:
        df = pd.read_json(main_data, orient='split')
        if drop_empty_row == [1]:
            for col in df.index:
                count = 0
                for i in df.isnull().values[df.index.get_loc(col)]:
                    if i:
                        count = count+1
                if count == df.columns[1:].size:
                    df=df.drop(col)

        options=[]
        if choosen_index == 'new':
            i=0
            for row in df.index.values:
                i = i + 1
                row = str(row) + ' (Zeile: ' + str(i) + ')' 
                options.append({'label':'{}'.format(row, row), 'value':(i-1)})
        else:
            i=0
            for row in df[choosen_index].values:
                i = i + 1
                if isinstance(row, list):
                    row = str(row[0]) + ' (Zeile: ' + str(i) + ')' 
                else: 
                    row = str(row) + ' (Zeile: ' + str(i) + ')' 
                options.append({'label':'{}'.format(row, row), 'value':(i-1)})
        return options
    else: return options


@app.callback([Output('prepared_data', 'data'), Output('get-data', 'children'), Output('get-data-informations', 'children'), 
                Output({'type':'errorView', 'index':0},'style'), Output('data-preparation', 'style')],
               [Input('main_data', 'data'), Input('index-dropdown','value'), Input('drop-col-dropdown', 'value'), 
               Input('drop-row-dropdown', 'value'), Input('empty-col-check', 'value'), Input('empty-row-check', 'value')])
def prepare_data(main_data, choosen_index, list_drop_col, list_drop_row, drop_empty_col, drop_empty_row):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    style3 = {'display':'flex'}
    
    if main_data is not None:
        df = pd.read_json(main_data, orient='split')
        if choosen_index == 'new':
            df=df.reset_index()
        elif choosen_index != 'new':
            df=df.set_index(choosen_index)
            df=df.reset_index()
        
        if list_drop_col is not None:
            df=df.drop(columns=list_drop_col)

        if list_drop_row is not None:
            
            for row in list_drop_row:
                if str(type(row)) == "<class 'int'>":
                    df=df.drop(row)

        str_list_empty_row =''
        for col in df.index:
            count = 0
            for i in df.isnull().values[df.index.get_loc(col)]:
                if i:
                    count = count+1
            if count == df.columns[1:].size:
                str_list_empty_row = str_list_empty_row + '"' + str(col+1) + '"; '
                if drop_empty_row == [1]:
                    str_list_empty_row = ' - '
                    df=df.drop(col)
                
        
        if str_list_empty_row == '':
            str_list_empty_row = ' - '
        
        if drop_empty_row == [1]:
            str_list_empty_row = ' - '
        
        str_list_empty_col =''
        str_list_col_high_nan ='| '

        for col, col_count in zip(df.columns, df.isnull().sum()):
            if round((col_count/df.index.size)*100) == 100:
                str_list_empty_col = str_list_empty_col + '"' + col + '"; '
            if round((col_count/df.index.size)*100) == 100 and drop_empty_col == [1]:
                str_list_empty_col = " - "
                df=df.drop(columns=col)
            elif round((col_count/df.index.size)*100) >= 50:
                str_list_col_high_nan = str_list_col_high_nan + '"' + col + '"' + ': ' + str(round((col_count/df.index.size)*100)) + '% | '


        count_values =(len(df.columns)*(len(df.index)))
        percent_float = (df.isnull().sum().sum()/count_values)
        percent_int = round(percent_float*100)
        
        children1 = tableFull(df)
        children2 = [
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
                    html.P('Anzahl leerer Zellen gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(df.isnull().sum().sum()) + ' (' + str(percent_int) + '%)', className='card-text2')
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Name von leeren Spalten: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str_list_empty_col, className='card-text2')
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Weitere Spalten mit hochem Anteil an leeren Zellen: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str_list_col_high_nan, className='card-text2')
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Leeren Zeilen: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str_list_empty_row, className='card-text2')
                ], style={'margin-left':'3px'})
                
            ], style={'text-align':'left'})]
        
        return df.to_json(date_format='iso', orient='split'), children1, children2, style2, style1
        
    
    else:
        return None, None, None, style1, style2


@app.callback(Output('main_data_after_preperation', 'data'),
              [Input('next-btn', 'n_clicks')],
              State('prepared_data', 'data'))
def get_new_main_data(next_btn, prepared_data):
    if next_btn:
        return prepared_data
    else: return None


def tableFull(df):
    children=[]
    if df is not None:
        children =[
             dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)
        ]
    return children  