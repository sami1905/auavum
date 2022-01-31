# from flask import Flask
# from dash_app import create_dash_app
import dash
import dash_bootstrap_components as dbc
#app = Flask(__name__)
app = dash.Dash(__name__, suppress_callback_exceptions=True,
                 external_stylesheets=[dbc.themes.BOOTSTRAP],
                 meta_tags=[{'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'}])
app.title = 'Auswertung und Analyse von Umfragen'



  
#create_dash_app(app)

server = app.server