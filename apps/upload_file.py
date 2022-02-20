from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
import sys
import pandas as pd
import base64
import io
import sys
import pandas as pd
from app import app

layout = dbc.Container([
    dcc.Store(id='raw_upload_data', storage_type='local'),
    dbc.Row([
        dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
        dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
        dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
    ] ,className='header'),

    dbc.Row([
        dbc.Col([], width=3),
        dbc.Col(html.Img(src='assets/img/progress1of4.png', className='progress-img'), width=6),
        dbc.Col(html.Div(id='output-alert-upload', style={'display':'none'}, className='upload-alert'),width=3)
    ], className='progress-row'),
    
    dbc.Row([
        dbc.Col(width=3),
        dbc.Col(
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    dbc.Card([
                        dbc.CardBody([
                            html.H1('Schritt 1: Daten hochladen'),
                            html.Img(src='/assets/img/file-upload.png', className='file-upload-img'),
                            html.P('Lade eine oder mehrere Dateien hoch, um mit der Auswertung und Analyse zu beginnen.',
                                className='card-text1',
                            ),
                            html.P(
                                'Datei(en) zum Hochladen hier per Drag & Drop ablegen',
                                className='card-text2',
                            ),
                            html.P(
                                'oder',
                                className='card-text2',
                            ),
                            dbc.Button('Datei(en) auswählen', id='upload-button', color='secondary', className='upload-button'),
                            
                        ]),
                    ], className='upload-card')
                ]),
            multiple=True),
        width=6),
        dbc.Col(width=3),
    ], className='file-upload'),

    
    
    dbc.Row([
        dbc.Col(html.Div([]),width=3),
        dbc.Col(
            html.Div([
                html.Hr(style={'margin': '5px', 'padding':'0'}),
                dbc.Row([
                    dbc.Col([
                        html.Div(html.Img(src='/assets/img/alert_info_icon_15x15.png', width='15px', height='15px')),
                        html.P('Hinweise: ', className='card-text3', style={'font-weight': 'bold', 'margin': '5px 0 0 0', 'padding':'0'}),

                    ])
                    
                ], className="default"),
                html.P('Gültige Formate - Zu den gültigen Dateiformaten zählen CSV und XLS(X).', className='card-text3', style={'margin': '5px 0 0 0', 'padding':'0'}),
                html.P('Datengröße - Lade maximal ein Gesamtvolumen von bis zu 1 MB hoch.', className='card-text3', style={'margin': '5px 0 0 0', 'padding':'0'}),
                html.P('CSV-Dateien - Bei der Auswertung von Dateien mit CSV-Format müssen die Spalten der Datei mit ";" getrennt sein. Andernfalls lassen sich hochgeladene CSV-Dateien nicht sauber auslesen.', className='card-text3', style={'margin': '5px 0 0 0', 'padding':'0'}),
                html.P('XLS(X)-Dateien - Beim Hochladen von XLS(X)-Dateien müssen Kennwörter von verschlüsselten Dateien entfernt werden. Außerdem ist lediglich das Auslesen eines einzelnen Excel-Blattes möglich. Enthält eine Datei mit einem XLS(X)-Format mehrere verschiedene Arbeitsblätter, wird lediglich das erste ausgelesen.', className='card-text3', style={'margin': '5px 0 0 0', 'padding':'0'}),
                html.P('Mehrere Dateien - Du kannst mehrere verschiedene Dateien in unterschiedlichen Dateiformaten hochladen. Beachte allerdings, dass die Dateien und ihre Inhalte die gleiche Struktur aufweisen, wenn Du die Inhalte der verschiedenen Dateien vertikal aneinanderhängen möchtest. Sollten die hochgeladenen Dateien unterschiedliche Datenstrukturen aufweise, werden sie horizontal verkettet.', className='card-text3', style={'margin': '5px 0 0 0', 'padding':'0'})
            ]), width=6),
        dbc.Col(html.Div([]),width=3),
        ], id='output-upload-info', className='upload-info'),
    
    html.Div([
        html.Hr(style={'margin': '8px 0 0 8px', 'padding':'0'}),
        dbc.Card([
                dbc.CardBody([
                    html.H2('Hochgeladene Dateien:'),
                    html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                    html.P('Wähle aus den hochgeladenen Dateien aus, welche Daten Du auswerten und analysieren möchtest:', className='card-text2', style={'margin': '10px 0 0 0','font-weight': 'bold'}),
                    dcc.Dropdown(
                        id='choice-data',
                        options=[
                            {'label': 'value 1', 'value': 1},
                            {'label': 'value 2', 'value': 2},
                            {'label': 'value 3', 'value': 3},
                        ],
                        optionHeight=35,
                        clearable=False,
                        value=[1],
                        searchable=False,
                        multi=True,
                        placeholder='Du hast keine Daten ausgwählt...',
                        className='dropdown',
                        style={'margin': '5px 0 0 0'}
                    ),
                    html.P('Enthält die Tabelle der ausgewählten Daten bereits Überschriften?', className='card-text2', style={'margin': '10px 0 0 0','font-weight': 'bold'}),
                    dcc.Checklist(id='check-header', 
                                            options=[{'label': '   Tabelle hat Überschriften', 'value': 1}],
                                            value=[1],
                                            className='checklist',
                                            style={'margin': '5px 0 0 5px'}
                                            )
                    
                ])    
            ], className='data-card')
    ], id='output-information-upload', className='output-data', style={'display':'none'}),
    html.Div(id='output-data-upload', className='output-data', style={'display':'none'}),   
], className='content', fluid=True)





# update main-data when data uploaded
@app.callback([Output('raw_upload_data', 'data'),
                Output('output-alert-upload', 'children'),
                Output('output-alert-upload', 'style')],
              [Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified')])
def add_upload_data(list_of_contents, list_of_names, list_of_dates):
    style1 = {'display':'block'}
    data=[]
    filenames=[]
    img_filename=[]
    wrong_filename=[]

    if list_of_contents is not None:
        for c, n, d in zip(list_of_contents, list_of_names, list_of_dates):
            
            #if get_dataFrame(c,n,d) is None:
                #return None
            if isinstance(content2df(c, n, d), str):
                wrong_filename.append(content2df(c, n, d))
                img_filename.append(None)
            elif isinstance(content2df(c, n, d), list):
                data.append(content2df(c, n, d)[0].to_json(date_format='iso', orient='split'))
                filenames.append(content2df(c, n, d)[1])
            else: return None, None, style1
        #data = data.to_json(date_format='iso', orient='split')
        

        for name in filenames:
            if '.csv' in name:
                img_filename.append('/assets/img/csv_icon.png')
            elif '.xls' in name:
                img_filename.append('/assets/img/xls_icon.png')
            if '.xls' not in name and '.csv' not in name:
                wrong_filename.append(str(name))
                img_filename.append(None)
                
        if not wrong_filename:
            children=[
                dbc.Alert([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Img(src='/assets/img/alert_success_icon_15x15.png', width='15px', height='15px')
                            ]),
                            html.P('Das Hochladen der Datei(en) war erfolgreich!', className='card-text2')

                        ])
                        
                    ], className='alert-headline'),
                    html.Hr(style={'padding':'0', 'margin':'0'}),
                    html.P('Eine Übersicht der hochgeladenen Datei(en) und ein Ausschnitt ihrer Inhalte werden nun dargestellt. Du kannst in der Übersicht Dateien entfernen und wieder hinzufügen oder erneut welche hochladen.', className='card-text3', style={'margin':'3px'})    
                ])
            ]
            liste = [data, filenames, img_filename]
            
            
    
            return liste, children, style1
        
        else:
            children = [
                dbc.Alert([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Img(src='/assets/img/alert_error_icon_15x15.png', width='15px', height='15px'),
                            ]),
                            html.P('Das Hochladen der Datei(en) ist fehlgeschlagen!', className='card-text2')
                        ])
                    ], className='alert-headline'),
                    html.P('Fehlerhafte Datei(en): ', className='card-text3', style={'margin': '0px'}),
                    html.Div(children=getFilename(img_filename, wrong_filename), style={'padding':'0', 'margin':'0'}),
                    html.Hr(style={'padding':'0', 'margin':'0'}),
                    html.P('Prüfe das Datenformat oder entferne Kennwörter der Datei(en) und versuche es erneut. Sollte das Format der Datei(en) korrekt und diese nicht mit einem Kennwort verschlüsselt sein, sind die Daten möglicherweise zu groß oder fehlerhaft!', className='card-text3', style={'margin':'3px'})
                ], color='danger')]
            
            return None, children, style1

    else:
        return None, None, style1

# update the output-information-upload   
@app.callback([Output('choice-data', 'options'), Output('choice-data', 'value')],
                [Input('raw_upload_data', 'data')],
                [State('choice-data', 'options'), State('choice-data', 'value')])
def update_options(raw_upload_data, options, value):
    if raw_upload_data is not None:
        filenames=raw_upload_data[1]
        img_filename = raw_upload_data[2]
        
        options=getFilename(img_filename, filenames)
        value=[]
        for i in filenames:
            value.append(filenames.index(i))
        return options, value 
    else: 
        return options, value 

# update the output-data-upload   
@app.callback([Output('output-data-upload', 'children'),Output('main_data', 'data'),
                Output('output-data-upload', 'style'), Output('output-information-upload', 'style'), 
                Output('output-upload-info', 'style')],
                [Input('raw_upload_data', 'data'), Input('choice-data', 'value'), Input('check-header', 'value')])
def add_data_output(raw_upload_data, choice_data, check_header):
    style1 = {'display':'block'}
    style2 = {'display':'none'}
    style3 = {'display':'flex'}
    
    if raw_upload_data is not None:
        upload = raw_upload_data[0]
        df = pd.DataFrame()
        index=choice_data

        for i in upload:
            for x in index:
                if x == upload.index(i):
                    df = df.append(pd.read_json(i, orient='split'))
        
        

    
        if len(index) == 0 or len(df.index) == 0 or len(df.columns) == 0:
            children = [
                dbc.Card([
                    dbc.CardBody([
                        html.H2('Übersicht: '),
                        html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                        dbc.Row([
                            dbc.Col(
                                html.Div([
                                    dbc.Row([
                                        html.P('Anzahl der ausgewählten Dateien: ', className='card-text2', style={'font-weight': 'bold'}),
                                        html.P(str(len(index)), className='card-text2')
                                    ]),
                                    dbc.Row([
                                        html.P('Anzahl der Zeilen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                                        html.P(str(len(df.index)), className='card-text2')
                                    ]),
                                    dbc.Row([
                                        html.P('Anzahl der Spalten gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                        html.P(str(len(df.columns)), className='card-text2')
                                    ])
                                ], style={'margin':'0 0 0 15px'}),
                                width=11),
                            dbc.Col(
                                dbc.Button('Weiter', color='secondary', outline=True, 
                                            style={'background': '#f2f2f2',
                                                'color' : '#3c4143',
                                                'position': 'absolute',
                                                'textAlign': 'center',
                                                'top' : '5px',
                                                'right': '15px'
                                                }),
                                style={'position':'relative'}, width=1)
                        ]),
                        html.H2('Ausschnitt der Datengesamtheit: '),
                        html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}), 
                        html.Div([
                            html.H1('Du hast keine Daten ausgewählt!', style={'font-size':'30px'}),
                            html.H1('Lade neue Dateien hoch oder wähle aus den bereits hochgeladenen Daten aus, um fortfahren zu können.', style={'font-size':'20px'})
                        ], className='empty-table', style={'margin-top':'10px'})
                    ])    
                ], className='data-card')
            ]
        else:
            if not check_header:
                list_header=[]
                first_row=[]
                df_without_header=df
                count_col=0
                for col in df_without_header.columns:
                    count_col = count_col + 1
                    list_header.append('Spalte ' + str(count_col))
                    first_row.append([col])
                df=pd.DataFrame(columns=list_header)
                df_without_header.columns=list_header
                df.loc[0]=first_row
                df=df.append(df_without_header, ignore_index=True)
            children = [
                dbc.Card([
                    dbc.CardBody([
                        html.H2('Übersicht: '),
                        html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                        dbc.Row([
                            dbc.Col(
                                html.Div([
                                    dbc.Row([
                                        html.P('Anzahl der ausgewählten Dateien: ', className='card-text2', style={'font-weight': 'bold'}),
                                        html.P(str(len(index)), className='card-text2')
                                    ]),
                                    dbc.Row([
                                        html.P('Anzahl der Zeilen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                                        html.P(str(len(df.index)), className='card-text2')
                                    ]),
                                    dbc.Row([
                                        html.P('Anzahl der Spalten gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                                        html.P(str(len(df.columns)), className='card-text2')
                                    ])
                                ], style={'margin':'0 0 0 15px'}),
                            width=11),
                            dbc.Col(    
                                dcc.Link(dbc.Button('Weiter', color='secondary', 
                                            style={'position': 'absolute',
                                                'textAlign': 'center',
                                                'top' : '5px',
                                }), 
                                            href='/daten-vorbereiten'),
                                style={'position':'relative'}, width=1)
                            ]), 
                            html.H2('Ausschnitt der Datengesamtheit: '),
                            html.Hr(style={'margin': '0 0 10px 0', 'padding':'0'}),
                            html.Div(children=tableHead(df))
                            ])    
                    ], className='data-card')]
        df=df.to_json(date_format='iso', orient='split')
        return children, df, style1, style1, style2 
        
    else:
        return None, None, style2, style2, style3





def tableHead(df):
    children=[]
    if df is not None:
        children =[
            dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True, responsive=True, style={'margin-bottom':'0', 'margin-top':'10px'}),
            dbc.Card([
                html.P('. . .', className='card-text', style={'text-align' : 'center', 'font-weight': 'bold', 'font-size':'30px', 'margin-top':'0'})
            ])
        ]
    return children    




def getFilename(img, name):
    if img[0] is None:
        children=[]
        for i in name:
            children.append(html.Li(i, className='card-text3', style={'padding':'0', 'margin':'0'}))
        return html.Ul(children) 
    else:
        children=[]
        for i in name:
            item={'label': i, 'value': name.index(i)}
            children.append(item)
        return children

# return uploaded content as dataframe
def content2df(contents, filename, date):
    content_type, content_string = contents.split(',')
    file_size= ((sys.getsizeof(contents)/1024)/1024)
    #print(filename + ': ' + str(file_size) + ' MB')
    decoded = base64.b64decode(content_string)

    try:
        if '.csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('latin1')), sep=';', low_memory=False)
            list = [df, filename]
            file_size= ((sys.getsizeof(df)/1024)/1024)
            #print('DataFrame: ' + str(file_size) + ' MB')
            return list
        elif '.xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            file_size= ((sys.getsizeof(df)/1024)/1024)
            #print('DataFrame: ' + str(file_size) + ' MB')
            list = [df, filename]
            return list
        elif '.xls' not in filename and '.csv' not in filename:
            return filename
    except Exception as e:
        print(e)
        return filename