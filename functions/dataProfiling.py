import plotly.express as px
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc

import functions.getTable as tableFuncs

def getCorr(df):
    corr= df.corr()
    fig = px.imshow(corr)
    return fig

def showOverview(df):
    count_empty_cols = 0
    count_empty_rows = 0

    for col in df.index:
        count = 0
        for i in df.isnull().values[df.index.get_loc(col)]:
            if i:
                count = count+1
        if count == df.columns[1:].size:
            count_empty_rows = count_empty_rows + 1
        
    for col, col_count in zip(df.columns, df.isnull().sum()):
        if round((col_count/df.index.size)*100) == 100:
            count_empty_cols = count_empty_cols + 1
        
    count_values =(len(df.columns)*(len(df.index)))
    empty_cells_percent_float = (df.isnull().sum().sum()/count_values)
    empty_cells_percent_int = round(empty_cells_percent_float*100)

    empty_cols_percent_float = (count_empty_cols/len(df.columns))
    empty_cols_percent_int = round(empty_cols_percent_float*100)

    empty_rows_percent_float = (count_empty_rows/len(df.index))
    empty_rows_percent_int = round(empty_rows_percent_float*100)

    children = dbc.Row([
            dbc.Col([
                html.H1("Allgemeine Informationen"),
                html.Hr(style={'margin': '0 0 30px 0', 'padding':'0'}),
                dbc.Row([
                    html.P('Anzahl der Zeilen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(len(df.index)), className='card-text2'),
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Anzahl leerer Zeilen: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(count_empty_rows) + ' (' + str(empty_rows_percent_int) + '%)', className='card-text2')
                ], style={'margin-left':'3px'}),
                    
                html.Hr(style={'margin': '0 0 15px 0', 'padding':'0'}),

                dbc.Row([
                    html.P('Anzahl der Spalten gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(len(df.columns)), className='card-text2'),
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Anzahl leerer Spalten: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(count_empty_cols) + ' (' + str(empty_cols_percent_int) + '%)', className='card-text2')
                ], style={'margin-left':'3px'}),
                    
                html.Hr(style={'margin': '0 0 15px 0', 'padding':'0'}),

                dbc.Row([
                    html.P('Anzahl Zellen gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(count_values), className='card-text2')
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Anzahl leerer Zellen gesamt: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(df.isnull().sum().sum()) + ' (' + str(empty_cells_percent_int) + '%)', className='card-text2')
                ], style={'margin-left':'3px'}),
                
                html.Hr(style={'margin': '0 0 15px 0', 'padding':'0'}),
            ], width=6),   
            dbc.Col([
                html.H1("Korrelation"),
                html.Hr(style={'margin': '0 0 30px 0', 'padding':'0'}),
                dcc.Graph(id='corr')
            ],width=6)
        ], style={'text-align':'left'})

    return children

def getCollapseInput(df, col):
    df_value_counts = df[col].value_counts().rename_axis('Antworten').reset_index(name='Anzahl')
    fig1 = px.bar(df[col].value_counts())
    fig1.update_layout(title =col, xaxis_title=col + " Antworten", yaxis_title='Anzahl')
    fig1.layout.update(showlegend=False)
    fig2 = px.histogram(df, x=col, barmode='group')
    fig2.update_layout(title =col + " gruppiert nach Kurs-Beschreibung", xaxis_title=col + " Antworten", yaxis_title='Anzahl')
    fig3 = px.pie(df.fillna('Keine Angaben'), df[col].fillna('Keine Angaben'))
    fig3.update_layout(title ='Verteilung: ' + col)         
    
    children = dbc.Row([
        dbc.Col(width = 4),
        dbc.Col(
            #dcc.Graph(figure = fig3),
            #dcc.Graph(figure = fig3)
            width = 4),
        dbc.Col(width = 4)
        
    ], style={'background':'white', 'margin': '20px', 'padding':'10px'})

    return children

    # return [dbc.Col(width = 4),
    #         dbc.Col([
    #             tableFuncs.tableFull(df_value_counts),
    #             dcc.Graph(figure = fig3)],width = 4),
    #         dbc.Col([
    #             dcc.Graph(figure = fig1),
    #             html.Hr(style={'margin': '5px 0', 'padding':'0'}),
    #             dcc.Graph(figure = fig2)], width =4)]
    
    

def getCollapseInputFloat(df, col, df_c):
    df_value_counts = df[col].value_counts().rename_axis('Antworten').reset_index(name='Anzahl')
    fig1 = px.bar(df[col].value_counts())
    fig1.update_layout(title =col, xaxis_title=col + " Antworten", yaxis_title='Anzahl')
    fig1.layout.update(showlegend=False)
    fig2 = px.histogram(df, x=col, barmode='group')
    fig2.update_layout(title =col + " gruppiert nach Kurs-Beschreibung", xaxis_title=col + " Antworten", yaxis_title='Anzahl')
    fig3 = px.pie(df.fillna('Keine Angaben'), df[col].fillna('Keine Angaben'))
    fig3.update_layout(title ='Verteilung: ' + col)         
    
    children = [dbc.Col([
                dbc.Row([
                    html.P('Anzahl der Zeilen gesamt: ', className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(len(df.index)), className='card-text2'),
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Anzahl der ausgefüllter Zeilen: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(len(df_c.index)), className='card-text2'),
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Anzahl leerer Zeilen: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(len(df.index)-len(df_c.index)), className='card-text2')
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Median: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(df[col].median()), className='card-text2')
                ], style={'margin-left':'3px'}),
                dbc.Row([
                    html.P('Durchschnitt: ' , className='card-text2', style={'font-weight': 'bold'}),
                    html.P(str(df[col].mean()), className='card-text2')
                ], style={'margin-left':'3px'})
            ], width = 4, style={'margin-top': '20px'}),
                                    
            dbc.Col([
                dbc.Table.from_dataframe(df_value_counts, striped=True, bordered=True, hover=True, responsive=True, style={'background': 'white', 'margin-top': '20px'}),
                dcc.Graph(figure = fig3)],width = 4),
            dbc.Col([
                dcc.Graph(figure = fig1),
                html.Hr(style={'margin': '5px 0', 'padding':'0'}),
                dcc.Graph(figure = fig2)], width =4)

            ]

    return children



    # for categorie in listOfFest:
        #     index= index+1
        #     cat = df[categorie]
        
        #     df_value_counts = df[categorie].value_counts().rename_axis('Antworten').reset_index(name='Anzahl')
        #     if cat.dtype == "float64":
        #         cat.sort_values
        #         df_value_counts=df_value_counts.sort_values(by=['Antworten'])
        #         df = df.sort_values(by=categorie)
        
            
        #     df_value_counts = df_value_counts.fillna('Keine Angaben')
       
            # if cat.dtype == "float64":
            #     df_c = df.dropna(subset=[categorie])
            #     new_collapse = html.Div([
            #          html.H2(categorie, id={'type':'dynamic-btn', 'index': index},
            #              n_clicks=0,
            #              style={'background': '#f2f2f2', 'color' : '#3c4143', 'width':'max',
            #              "border-bottom": "2px #3c414350 solid", "padding": "20px 10px", "margin" : "0"}
            #          ),
            #         dbc.Collapse([], style={'background': '#3c414330', 'color' : '#3c4143', 'width':'max','margin':'-2px 0 0 0', "padding":"15px", "border-bottom": "2px #3c414350 solid"},
            #             id={'type':'profile-collapse', 'index': index},
            #             is_open=False
            #         )
                    
            #      ], style={'text-align':'left'})