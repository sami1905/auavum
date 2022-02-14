from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def profile(data, col):
    
    return getContent(data, col)



def getContent(df, col):
    if df[col].dtype == "float64":
        cat = df[col]
        df_value_counts = cat.value_counts().rename_axis('Antworten').reset_index(name='Anzahl')
                
        cat.sort_values
        df_value_counts=df_value_counts.sort_values(by=['Antworten'])
        df_c = df.dropna(subset=[col])
        #df = df.sort_values(by=categorie)
        return getCollapseInputFloat(df, col, df_c)

                
                
    else:
        df_c = df.dropna(subset=[col])
        return getCollapseInput(df, col, df_c)
    

def getCollapseInput(df, col, df_c):
    df_value_counts = df[col].value_counts().rename_axis('Antworten').reset_index(name='Anzahl')
    fig1 = px.bar(df[col].value_counts())
    fig1.update_layout(title =col, xaxis_title=col + " Antworten", yaxis_title='Anzahl')
    fig1.layout.update(showlegend=False)
    fig2 = px.pie(df.fillna('Keine Angaben'), df[col].fillna('Keine Angaben'))
    fig2.update_layout(title ='Verteilung: ' + col)         
    
    return html.Div([
        html.H1(col, style={'margin-top':'25px'}),
        dbc.Row([
            dbc.Col(
                html.Div([
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
                    dcc.Graph(figure = fig1),
                    dcc.Graph(figure = fig2)
                ]),width = 6),
            dbc.Col(
                tableFull(df_value_counts), width = 6),
        ])
    ], style={'margin-top':'20px','padding':'10 px'})


def tableFull(df):
    children=[]
    if df is not None:
        children =[
             dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)
        ]
    return children    

def getCollapseInputFloat(df, col, df_c):
    df_value_counts = df[col].value_counts().rename_axis('Antworten').reset_index(name='Anzahl')
    fig1 = px.bar(df[col].value_counts())
    fig1.update_layout(title =col, xaxis_title=col + " Antworten", yaxis_title='Anzahl')
    fig1.layout.update(showlegend=False)
    fig2 = px.pie(df.fillna('Keine Angaben'), df[col].fillna('Keine Angaben'))
    fig2.update_layout(title ='Verteilung: ' + col)         
    
    children = html.Div([
        html.H1(col, style={'margin-top':'25px'}),
        dbc.Row([
            dbc.Col(
                html.Div([
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
                    ], style={'margin-left':'3px'}),
                    dcc.Graph(figure = fig1),
                    dcc.Graph(figure = fig2)
                    ]), width = 6, style={'margin-top': '20px'}),
                                            
            dbc.Col(
                tableFull(df_value_counts), width = 6),

            ])
        ], style={'margin-top':'20px','padding':'10 px'})

    return children