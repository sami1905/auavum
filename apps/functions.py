import plotly.express as px
import plotly.figure_factory as ff
from scipy.spatial.distance import pdist, squareform
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import plotly.graph_objects as go
from app import vectorizer
from summarizer import Summarizer
import torch
from transformers import AutoTokenizer, AutoModel
# from wordcloud import STOPWORDS
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize

# german_stop_words = stopwords.words('german')
# text_file = open('./assets/txt/stopwords.txt', 'r', encoding='utf-8')
# swords = text_file.read()
# text_file.close()
# liste_der_unerwuenschten_woerter = swords.split()
# STOPWORDS.update(german_stop_words)
# STOPWORDS.update(liste_der_unerwuenschten_woerter)

summary_model=Summarizer()
tokenizer = AutoTokenizer.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
token_model = AutoModel.from_pretrained('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

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


def get_Dendro(vectors, labels):

    # Initialize figure by creating upper dendrogram
  
    dendro = ff.create_dendrogram(vectors, orientation='bottom', labels=labels, linkagefun=lambda x: sch.linkage(x, "complete", "euclidean"))
    for i in range(len(dendro['data'])):
        dendro['data'][i]['yaxis'] = 'y2'
        
    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(vectors, orientation='right')
    for i in range(len(dendro_side['data'])):
        dendro_side['data'][i]['xaxis'] = 'x2'
            
    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        dendro.add_trace(data)
        
    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        dendro.add_trace(data)
        
    # Create Heatmap
    dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    dendro_leaves = list(map(int, dendro_leaves))

    data_dist = pdist(vectors)
    heat_data = squareform(data_dist)
    heat_data = heat_data[dendro_leaves,:]
    heat_data = heat_data[:,dendro_leaves]

    heatmap = [
        go.Heatmap(
            x = dendro_leaves,
            y = dendro_leaves,
            z = heat_data,
            colorscale = 'Blues'
        )]
        
    heatmap[0]['x'] = dendro['layout']['xaxis']['tickvals']
    heatmap[0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # Add Heatmap Data to Figure
    for data in heatmap:
        dendro.add_trace(data)

    # Edit Layout
    dendro.update_layout({'width':1200, 'height':1200,
                            'showlegend':False, 'hovermode': 'closest',
                            })

    # Edit xaxis
    dendro.update_layout(xaxis={'domain': [.15, 1],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'ticks':""})
    # Edit xaxis2
    dendro.update_layout(xaxis2={'domain': [0, .15],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'showticklabels': False,
                                        'ticks':""})

    # Edit yaxis
    dendro.update_layout(yaxis={'domain': [0, .85],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'showticklabels': False,
                                        'ticks': ""
                                })
    # Edit yaxis2
    dendro.update_layout(yaxis2={'domain':[.825, .975],
                                        'mirror': False,
                                        'showgrid': False,
                                        'showline': False,
                                        'zeroline': False,
                                        'showticklabels': False,
                                        'ticks':""})   

    return dendro

def get_Clusters(k, vectors):
    Hclustering = AgglomerativeClustering(n_clusters=k, affinity='euclidean', linkage='complete')
    Hclustering.fit(vectors)
    return Hclustering.labels_

def transformation(sentences):
    print("in old_transformation Funktion")
    vectorizer.bert(sentences)
    vectors = vectorizer.vectors

    return vectors


#Mean Pooling - Take attention mask into account for correct averaging
def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] #First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)

def new_transformation(sentences):
    #listfosents=[]
    # for sent in sentences:
    #     text_tokens = word_tokenize(sent)
    #     tokens_without_sw = [word for word in text_tokens if not word in STOPWORDS]

    #     listfosents.append((" ").join(tokens_without_sw))


    # Tokenize sentences
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

    # Compute token embeddings
    with torch.no_grad():
        model_output = token_model(**encoded_input)

    # Perform pooling. In this case, max pooling.
    sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])
    list = sentence_embeddings

    return list

def summary(text):
    return summary_model(text, num_sentences=3)