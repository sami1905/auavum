import dash_bootstrap_components as dbc
from dash import dcc
from dash import html


layout = dbc.Container([
    html.Div([
        dbc.Row([
        dbc.Col(dcc.Link(html.Img(src='/assets/img/logo_smartistics40x40.png', height='40px'), href='/'), width=1),
        dbc.Col(html.H1('Auswertung und Analyse von Umfragen'), width=10),
        dbc.Col(html.Img(src='/assets/img/bwi-logo_84x40.png', height='40px'), className='header_logo_bwi', width=1)
        ] ,className='header'),
        html.H1('Wartungsmodus', style={'font-size':'100px', 'margin':'40px'}),
        html.Img(src='../assets/img/wartung800x711.png', width=600),
        html.H1('Wir sind bald zurück!', style={'font-size':'30px', 'margin':'30px'}),
        html.P('Die Website ist aktuell aufgrund von Wartungsarbeiten nicht erreichbar.', className='card-text1', style={'margin-bottom':'20px'})
    ], className='alert-wrapper')
], className='content', fluid=True)

