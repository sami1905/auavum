from re import I
from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from app import app
from textblob_de import TextBlobDE as TextBlob
import pandas as pd
import plotly.express as px
from functions import sentimentModel

sentModel = sentimentModel.GSBertPolarityModel()

#tokenizer
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk



#lemmatization
import spacy
lemma = spacy.load('de_core_news_md')

#stopwords
text_file = open('./assets/txt/stopwords_sentiment.txt', 'r', encoding='utf-8')
swords = text_file.read()
text_file.close()
liste_der_unerwuenschten_woerter = swords.split()

german_stop_words = liste_der_unerwuenschten_woerter #+ stopwords.words('german')

def layout(text, index):
    
    
    children = dbc.Container([
        dcc.Store(id='sentiment-data', storage_type='memory', data=text),
        dcc.Store(id='sentiment-index', storage_type='memory', data=index),
        dcc.Store(id='sentiment-split', storage_type='memory', data=index),
        html.Div([
                        html.P('Wähle ein Sentiment-Modell aus:' , className='card-text2', style={'font-weight': 'bold'}),
                        dcc.Dropdown(id='sentmodel-dropdown', 
                                    	    options=[{'label': 'TextBlob DE (schnell und weniger genau)', 'value': 0},
                                            {'label': 'GSBertPolarityModel (langsam und genau)', 'value': 1}], 
                                            value=0, 
                                            clearable=False,
                                            searchable=False,
                                            multi=False,
                                            className='dropdown')

                    ], style={'text-align': 'left', 'margin': '0px, 30px'}),
        dbc.Row([
            dbc.Col(dcc.Checklist(id='check-sentiment', 
                                            options=[{'label': '   Freitexte in Sätze unterteilen', 'value': 1}],
                                            value=[],
                                            className='checklist',
                                            style={'margin': '5px 0 0 5px'}
                                            ), width=2),
            dbc.Col(width=4),
            dbc.Col(width=6)
        ]),
        dbc.Row([
            dbc.Col(html.Div([
                html.P("Polaritätsbereich: ", className='card-text1', style={'font-weight': 'bold'}),
                dcc.RangeSlider(id='pol-slider',
                    min=-1, max=1, step=0.05,
                    marks={-1: '-1', -0.5:'-0.5', 0:'0', 0.5:'0.5', 1: '1'},
                    value=[-1, 1]
                    )
                    ]), width=5),
            dbc.Col(width=1),
            dbc.Col(html.Div([
                html.P('Subjektivitätsbereich: ', className='card-text1', style={'font-weight': 'bold'}),
                dcc.RangeSlider(id='sub-slider',
                        min=0, max=1, step=0.05,
                        marks={0:'0', 0.5:'0.5', 1: '1'},
                        value=[0, 1]
                        ),

            ]), width=5)
        ], style={'margin': '20px'}),
        
        

        html.Div([], id="sentiment-content")
            
    ],style={'text-align':'left'}, fluid=True)
    return children

@app.callback([Output("sentiment-content", "children"),
            Output('listOfSentiment', 'data'),
            Output('sentiment-split', 'data')],
                [Input('pol-slider', 'value'),
                Input('sub-slider', 'value'),
                Input('check-sentiment', 'value'),
                Input('sentmodel-dropdown', 'value')],
                [State('sentiment-data', 'data'),
                State('sentiment-index', 'data')]
)
def get_sentiment(polvalues, subvalues, checkbox, smodel, texts, index):
    print(type(texts))
    
    # sentiment
    list_polarity = []
    list_subjektivity = []
    list_countCharts = []
    
    df_raw = pd.DataFrame({'Index': index,
                        'Text': texts})

    if checkbox == [1]:
        df_splited = pd.DataFrame(columns = ['Index', 'Text'])
        for i, p in df_raw.itertuples(index=False):

            sentence_token = nltk.tokenize.sent_tokenize(p)
            print(sentence_token)
            for t in sentence_token:
                data = pd.DataFrame({'Index': [i], 'Text': [t]})
                df_splited=df_splited.append(data)

        unfiltered_sentences = df_splited['Text'].values.tolist()
        
        

    
    else:
        unfiltered_sentences = texts
        
    filtered_sentences = []
    for sent in unfiltered_sentences:
        # tokenization
        sent_token = word_tokenize(sent)

        #removing special characters
        tokens_without_sc = []
        for token in sent_token:
            word = ''.join(e for e in token if e.isalnum())
            if word != '':
                tokens_without_sc.append(word)
        
        #removing stopwords
        #tokens_without_sc_an_sw = [word for word in tokens_without_sc if not word.lower() in german_stop_words]

        #lemmatization
        #lemma_tokens_without_sc_and_sw = []
        #for word in tokens_without_sc:
        #    doc = lemma(word)
        #    lemma_token = ' '.join([x.lemma_ for x in doc]) 
        #    lemma_tokens_without_sc_and_sw.append(lemma_token)
        
        
        curr_sent = (" ").join(tokens_without_sc)
        filtered_sentences.append(curr_sent)

    
    if smodel == 0:

        #old
        for text in filtered_sentences:
            blob = TextBlob(text)
            list_polarity.append(blob.sentiment.polarity)
            list_subjektivity.append(blob.sentiment.subjectivity)
            list_countCharts.append(len(text))
    else:    
        #new
        for text in filtered_sentences:
            p = round(sentModel.analyse_sentiment(text), 2)
            list_polarity.append(p)
            list_subjektivity.append(0)
            list_countCharts.append(len(text))

    if checkbox == [1]:
        df = df_splited.copy()
        df['Polarität'] = list_polarity
        df['Subjektivität'] = list_subjektivity
        df['Anzahl Zeichen'] = list_countCharts
    
    else:
        df = pd.DataFrame({'Index': index,
                        'Text': texts,
                        'Polarität': list_polarity,
                        'Subjektivität': list_subjektivity,
                        'Anzahl Zeichen': list_countCharts})

    df_output = df.copy()
    
    pos = []
    neu = []
    neg = []

    pollow, polhigh = polvalues
    sublow, subhigh = subvalues
    maskpol = (df['Polarität'] >= pollow) & (df['Polarität'] <= polhigh)
    df = df[maskpol]

    masksub = (df['Subjektivität'] >= sublow) & (df['Subjektivität'] <= subhigh)
    df = df[masksub]
    
    df=df.reset_index()
    for row in df.index:
        if df.iloc[row]['Polarität'] > 0:
            pos.append(row)

        elif df.iloc[row]['Polarität'] < 0:
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

    
    posTabl = []
    neuTabl = []
    negTabl = []
    

    for row in df_pos.index:
        pol = int(round(df_pos.iloc[row]['Polarität'] *100))
        
        if pol == 100:
            colorpol = "#008800"
            

        else:
            colorpol = "#008800" + str(pol)

        chartpos = html.P(str(round(df_pos.iloc[row]['Polarität'], 2)), style={'text-align' : 'center',
                                                                        'padding-top':'6px',
                                                                        'font-size' : '15px',
                                                                        'font-weight': 'bold', 
                                                                        'width': '40px', 
                                                                        'height':'40px',
                                                                        'border' : '3px #004600 solid',
                                                                        'border-radius': '25px',
                                                                        'color': '#004600',
                                                                        'background': colorpol} )
        
        sub = int(round(df_pos.iloc[row]['Subjektivität'] *100))
        
        if sub == 100:
            colorsub = "#3c4143"
            
        elif sub < 10:
            colorsub = "#3c414310"
        else:
            colorsub = "#3c4143" + str(sub)
        
        chartsub = html.P(str(round(df_pos.iloc[row]['Subjektivität'], 2)), style={'text-align' : 'center',
                                                                        'padding-top':'6px',
                                                                        'font-size' : '15px',
                                                                        'font-weight': 'bold', 
                                                                        'width': '40px', 
                                                                        'height':'40px',
                                                                        'border' : '3px #000000 solid',
                                                                        'border-radius': '25px',
                                                                        'color': '#000000',
                                                                        'background': colorsub} )

        
        posTabl.append(html.P('Text: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '15px'}))
        posTabl.append(html.P(df_pos.iloc[row]['Text'], className='card-text2', style={'margin-top': '5px'}))
        posTabl.append(dbc.Row([dbc.Col(html.Div([html.P('Polarität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}), chartpos])), dbc.Col(html.Div([html.P('Subjektivität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}), chartsub]))]))
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
            colorpol = "#FFFFFF"
        
        chartpos = html.P(str(round(df_neu.iloc[row]['Polarität'], 2)), style={'text-align' : 'center',
                                                                        'padding-top':'6px',
                                                                        'font-size' : '15px',
                                                                        'font-weight': 'bold', 
                                                                        'width': '40px', 
                                                                        'height':'40px',
                                                                        'border' : '3px #3c4143 solid',
                                                                        'border-radius': '25px',
                                                                        'color': '#3c4143',
                                                                        'background': colorpol} )

        sub = int(round(df_neu.iloc[row]['Subjektivität'] *100))
        
        
        if sub == 100:
            colorsub = "#3c4143"
            
        elif sub < 10:
            colorsub = "#3c414310"
        else:
            colorsub = "#3c4143" + str(sub)
        
        chartsub = html.P(str(round(df_neu.iloc[row]['Subjektivität'], 2)), style={'text-align' : 'center',
                                                                        'padding-top':'6px',
                                                                        'font-size' : '15px',
                                                                        'font-weight': 'bold', 
                                                                        'width': '40px', 
                                                                        'height':'40px',
                                                                        'border' : '3px #000000 solid',
                                                                        'border-radius': '25px',
                                                                        'color': '#000000',
                                                                        'background': colorsub} )

        
        neuTabl.append(html.P('Text: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '15px'}))
        neuTabl.append(html.P(df_neu.iloc[row]['Text'], className='card-text2', style={'margin-top': '5px'}))
        neuTabl.append(dbc.Row([dbc.Col(html.Div([html.P('Polarität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}), chartpos])), dbc.Col(html.Div([html.P('Subjektivität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}), chartsub]))]))
        neuTabl.append(html.Hr(style={'margin': '5px 0 25px 0', 'padding':'0'}))
    

    for row in df_neg.index:
        pol = int(round(df_neg.iloc[row]['Polarität'] *100))
        
        

        if pol == -100:
            colorpol = "#ff0000"
        
        else:
            colorpol = "#ff0000" + str(pol*-1)

        chartpos = html.P(str(round(df_neg.iloc[row]['Polarität'], 2)), style={'text-align' : 'center',
                                                                        'padding-top':'6px',
                                                                        'font-size' : '15px',
                                                                        'font-weight': 'bold', 
                                                                        'width': '40px', 
                                                                        'height':'40px',
                                                                        'border' : '3px #3A0000 solid',
                                                                        'border-radius': '25px',
                                                                        'color': '#3A0000',
                                                                        'background': colorpol} )
        
        sub = int(round(df_neg.iloc[row]['Subjektivität'] *100))
        
        
        if sub == 100:
            colorsub = "#3c4143"
            
        elif sub < 10:
            colorsub = "#3c414310"
        else:
            colorsub = "#3c4143" + str(sub)
        
        chartsub = html.P(str(round(df_neg.iloc[row]['Subjektivität'], 2)), style={'text-align' : 'center',
                                                                        'padding-top':'6px',
                                                                        'font-size' : '15px',
                                                                        'font-weight': 'bold', 
                                                                        'width': '40px', 
                                                                        'height':'40px',
                                                                        'border' : '3px #000000 solid',
                                                                        'border-radius': '25px',
                                                                        'color': '#000000',
                                                                        'background': colorsub} )

        
        negTabl.append(html.P('Text: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '15px'}))
        negTabl.append(html.P(df_neg.iloc[row]['Text'], className='card-text2', style={'margin-top': '5px'}))
        negTabl.append(dbc.Row([dbc.Col(html.Div([html.P('Polarität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}), chartpos])), dbc.Col(html.Div([html.P('Subjektivität: ', className='card-text1', style={'font-weight': 'bold', 'margin-top': '25px'}), chartsub]))]))
        
        negTabl.append(html.Hr(style={'margin': '5px 0 15px 0', 'padding':'0'}))
    
    df = df.set_index(df.columns[0])
    fig_polarity = px.histogram(df, x='Polarität')
    fig_subjectivity = px.histogram(df, x='Subjektivität')
    fig_polarity.update_layout(yaxis_title='Anzahl')    
    fig_subjectivity.update_layout(yaxis_title='Anzahl')
    df['Text'] = df['Text'].str.wrap(30)
    df['Text'] = df['Text'].apply(lambda x: x.replace('\n', '<br>'))
    scatter = px.scatter(df, x='Polarität', y='Subjektivität', size='Anzahl Zeichen', hover_data=['Text', 'Index'])
    scatter.update_layout(yaxis_title='Subjektivität', xaxis_title='Polarität') 
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
                            html.H2('Positiv (' + str(len(pos)) + ')', style={'font-weight': 'bold'}),
                            html.Div(posTabl)
                            
                        ]),width=4), 
                    dbc.Col(
                        html.Div([
                            html.H2('Neutral (' + str(len(neu)) + ')', style={'font-weight': 'bold'}),
                            html.Div(neuTabl)
                        ]), width=4),
                    dbc.Col(
                        html.Div([
                            html.H2('Negativ (' + str(len(neg)) + ')', style={'font-weight': 'bold'}),
                            html.Div(negTabl)
                        ]), width=4)

                ]),width=7)
            
        ])

    ], style={"margin" : "20px"})

    return children, df_output.to_json(date_format='iso', orient='split'), checkbox

