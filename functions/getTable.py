import dash_bootstrap_components as dbc
from dash import html


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

def tableFull(df):
    children=[]
    if df is not None:
        children =[
             dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, responsive=True)
        ]
    return children    
