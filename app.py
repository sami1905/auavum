import dash
import dash_bootstrap_components as dbc
import pandas as pd



app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Auswertung und Analyse von Umfragen'

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

app.layout = dbc.Container([
    
    html.Div(id='max-screen', 
            children=[
                html.H1('Wartungsarbeiten!', style={'font-size':'100px', 'margin':'40px'}),
                html.H2('Die Anwendung steht in kürze bereit.', style={'font-size':'30px', 'margin':'30px'}),
            ], className='max-screen'),

            
], className='content', fluid=True)

server = app.server