from flask import Flask
#from dash_app import create_dash_app
import dash
import dash_bootstrap_components as dbc


#app = Flask(__name__)

server = Flask('app')
app = dash.Dash(__name__, server=server,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Auswertung und Analyse von Umfragen'


#create_dash_app(app)
  
from app import app
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

app.layout = dbc.Container([
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


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=True)
