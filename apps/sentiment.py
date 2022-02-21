
from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from app import app
from textblob_de import TextBlobDE as TextBlob
import pandas as pd
import plotly.express as px

def layout(text, index):
    
    
    children = dbc.Container([
        dcc.Store(id='sentiment-data', storage_type='memory', data=text),
        dcc.Store(id='sentiment-index', storage_type='memory', data=index),
        html.Div([], id="sentiment-content")
            
    ],style={'text-align':'left'}, fluid=True)
    return children

@app.callback(Output("sentiment-content", "children"), 
                [Input('sentiment-data', 'data'),
                Input('sentiment-index', 'data')]
)
def get_sentiment(texts, index):
    # sentiment
    list_polarity = []
    list_subjektivity = []
    list_countCharts = []
    
    for text in texts:
        blob = TextBlob(text)
        list_polarity.append(blob.sentiment.polarity)
        list_subjektivity.append(blob.sentiment.subjectivity)
        list_countCharts.append(len(text))

    df = pd.DataFrame({'Index': index,
                        'Text': texts,
                        'Polarität': list_polarity,
                        'Subjektivität': list_subjektivity,
                        'Anzahl Zeichen': list_countCharts})
    
    fig_polarity = px.histogram(df, x='Polarität')
    fig_subjectivity = px.histogram(df, x='Subjektivität')
    fig_polarity.update_layout(yaxis_title='Anzahl')    
    fig_subjectivity.update_layout(yaxis_title='Anzahl')
    
    pos = []
    neu = []
    neg = []
    for row in df.index:
        if df.iloc[row]['Polarität'] >= 0.25:
            pos.append(row)

        elif df.iloc[row]['Polarität'] <= -0.25:
            neg.append(row)
        else:
            neu.append(row)

    df_pos = df.iloc[pos]
    df_neu = df.iloc[neu]
    df_neg = df.iloc[neg]

    df_pos=df_pos.sort_values(by=['Polarität'], ascending=False)
    df_neu=df_neu.sort_values(by=['Polarität'], ascending=False)
    df_neg=df_neg.sort_values(by=['Polarität'])

    df_pos= df_pos.reset_index()
    df_neu=df_neu.reset_index()
    df_neg=df_neg.reset_index()

    
    df['Text'] = df['Text'].str.wrap(30)
    df['Text'] = df['Text'].apply(lambda x: x.replace('\n', '<br>'))
    scatter = px.scatter(df, x='Polarität', y='Subjektivität', size='Anzahl Zeichen', hover_data=['Text', 'Index'])
    scatter.update_layout(yaxis_title='Subjektivität', xaxis_title='Polarität') 

    posTabl = []
    neuTabl = []
    negTabl = []
    

    for row in df_pos.index:
        pol = int(round(df_pos.iloc[row]['Polarität'] *100))
        
        if pol == 100:
            colorpol = "#008800"
        else:
            colorpol = "#008800" + str(pol)
        
        sub = int(round(df_pos.iloc[row]['Subjektivität'] *100))
        
        if sub == 100:
            colorsub = "#3c4143"
        elif sub < 10:
            colorsub = "#3c414310"
        else:
            colorsub = "#3c4143" + str(sub)

        
        posTabl.append(html.P('Text: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '15px'}))
        posTabl.append(html.P(df_pos.iloc[row]['Text'], className='card-text2', style={'margin-top': '5px'}))
        posTabl.append(html.P('Polarität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}))
        posTabl.append(dbc.Progress(value=df_pos.iloc[row]['Polarität'], color=colorpol, max=1.0, style={'background-color':colorpol}))
        posTabl.append(html.P('Subjektivität: ', className='card-text1', style={'font-weight': 'bold','margin-top': '25px'}))
        posTabl.append(dbc.Progress(value=df_pos.iloc[row]['Subjektivität'], color=colorsub, max=1.0, style={'background-color':colorsub}))
        posTabl.append(html.Hr(style={'margin': '5px 0 15px 0', 'padding':'0'}))

    
    for row in df_neu.index:
        pol = int(round(df_neu.iloc[row]['Polarität'] *100))
        
        
        if pol <= -10:
            colorpol = "#ff0000" + str(pol* -1)
            value=(df_neu.iloc[row]['Polarität'] *-1)
        

        elif pol >= 10:
            colorpol = "#008800" + str(pol)
            value=df_neu.iloc[row]['Polarität']

        elif pol < 10 and pol > 0:
            colorpol = "#00880010" 
            value=df_neu.iloc[row]['Polarität']

        
        elif pol > -10 and pol < 0:
            colorpol = "#ff000010"
            value=(df_neu.iloc[row]['Polarität'] *-1)
        
        
        else:
            colorpol = "#3c4143"
            value=df_neu.iloc[row]['Polarität']
        
        
        sub = int(round(df_neu.iloc[row]['Subjektivität'] *100))
        
        if sub == 100:
            colorsub = "#3c4143"
        
        elif sub < 10:
            colorsub = "#3c414310"
 
        else:
            colorsub = "#3c4143" + str(sub)

        
        neuTabl.append(html.P('Text: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '15px'}))
        neuTabl.append(html.P(df_neu.iloc[row]['Text'], className='card-text2', style={'margin-top': '5px'}))
        neuTabl.append(html.P('Polarität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}))
        neuTabl.append(dbc.Progress(value=value, color=colorpol, max=1.0, style={'background-color': colorpol }))
        neuTabl.append(html.P('Subjektivität: ', className='card-text1', style={'font-weight': 'bold','margin-top': '25px'}))
        neuTabl.append(dbc.Progress(value=df_neu.iloc[row]['Subjektivität'], style={'background-color':colorsub}))
        neuTabl.append(html.Hr(style={'margin': '5px 0 25px 0', 'padding':'0'}))
    

    for row in df_neg.index:
        pol = int(round(df_neg.iloc[row]['Polarität'] *100))
        
        

        if pol == -100:
            colorpol = "#ff0000"
        
        else:
            colorpol = "#ff0000" + str(pol*-1)
        
        sub = int(round(df_neg.iloc[row]['Subjektivität'] *100))
        
        if sub == 100:
            colorsub = "#3c4143"
        elif sub < 10:
            colorsub = "#3c414310"
        else:
            colorsub = "#3c4143" + str(sub)

        
        negTabl.append(html.P('Text: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '15px'}))
        negTabl.append(html.P(df_neg.iloc[row]['Text'], className='card-text2', style={'margin-top': '5px'}))
        negTabl.append(html.P('Polarität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}))
        negTabl.append(dbc.Progress(value=df_neg.iloc[row]['Polarität'], color=colorpol, max=-1.0, style={'background-color': colorpol }))
        negTabl.append(html.P('Subjektivität: ', className='card-text1', style={'font-weight': 'bold','margin-top': '25px'}))
        negTabl.append(dbc.Progress(value=df_neg.iloc[row]['Subjektivität'], color=colorsub, max=1.0, style={'background-color': colorsub }))
        negTabl.append(html.Hr(style={'margin': '5px 0 15px 0', 'padding':'0'}))
    
    
    children=html.Div([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H2('Diagramme', style={'font-weight': 'bold'}),
                    dcc.Graph(figure = scatter),
                    dcc.Graph(figure = fig_polarity),
                    dcc.Graph(figure = fig_subjectivity),

                ]), width=5),
            dbc.Col(
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.H2('Positiv', style={'font-weight': 'bold'}),
                            html.Div(posTabl)
                            
                        ]),width=4), 
                    dbc.Col(
                        html.Div([
                            html.H2('Neutral', style={'font-weight': 'bold'}),
                            html.Div(neuTabl)
                        ]), width=4),
                    dbc.Col(
                        html.Div([
                            html.H2('Negativ', style={'font-weight': 'bold'}),
                            html.Div(negTabl)
                        ]), width=4)

                ]),width=7)
            
        ])

    ], style={"margin" : "20px"})

    return children    

