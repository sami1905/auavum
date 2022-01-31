# dash app
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


# app = dash.Dash(__name__, suppress_callback_exceptions=True,
#                 external_stylesheets=[dbc.themes.BOOTSTRAP],
#                 meta_tags=[{'name': 'viewport',
#                             'content': 'width=device-width, initial-scale=1.0'}])
# app.title = 'Auswertung und Analyse von Umfragen'

def create_dash_app(flask_app):
    dash_app =  dash.Dash(server=flask_app,name="auavum", 
                            url_base_pathname="/start/", 
                            external_stylesheets=[dbc.themes.BOOTSTRAP],
                            meta_tags=[{'name': 'viewport',
                                    'content': 'width=device-width, initial-scale=1.0'}])
    dash_app.title = 'Auswertung und Analyse von Umfragen'
    
    dash_app.layout = dbc.Container([
        # dcc.Location(id='url', refresh=False),
        # dcc.Store(id='main_data', storage_type='session'),
        # dcc.Store(id='main_data_after_preperation', storage_type='session'),
        # dcc.Store(id='listOfFrei', storage_type='session'),
        # dcc.Store(id='listOfFest', storage_type='session'),
        html.Div(id='page-content', children=[], className='page-content'),
        html.Div(id='max-screen', 
                children=[
                    html.H1('Das ist die Dash-App!', style={'font-size':'100px', 'margin':'40px'}),
                    #html.Img(src='../assets/img/max_size.png', height='400px'),
                    html.H2('Staaaaart!', style={'font-size':'30px', 'margin':'30px'}),
                    html.P('Yeeah.',
                className='card-text1')], className='max-screen'),

                
    ], className='content', fluid=True)
    return dash_app





