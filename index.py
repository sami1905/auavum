#127.0.0.1:5000
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

#connect to main app.py file and to apps
from app import app, server
from apps import upload_file



app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='main_data', storage_type='session'),
    dcc.Store(id='main_data_after_preperation', storage_type='session'),
    dcc.Store(id='listOfFrei', storage_type='session'),
    dcc.Store(id='listOfFest', storage_type='session'),
    html.Div(id='page-content', children=[], className='page-content'),
    html.Div(id='max-screen', 
            children=[html.H1('Fenstergröße anpassen!', style={'font-size':'100px', 'margin':'40px'}),
            #html.Img(src='../assets/img/max_size.png', height='400px'),
            html.H2('Bitte erhöhe die Größe Deines Internetbrowser-Fensters, um die Inhalte anzuzeigen.', style={'font-size':'30px', 'margin':'30px'}),
            html.P('Um eine optimale Übersicht der Auswertung und Analyse erhalten zu können, empfiehlt es sich Deinen Internetbrowser-Fenster zu maximieren.',
            className='card-text1')], className='max-screen'),

            
], className='content', fluid=True)

## File-Structure

@app.callback(Output(component_id='page-content', component_property='children'),
                 [Input(component_id='url',component_property='pathname')])
def display_page(pathname):
     if pathname == '/':
        return upload_file.layout
#     if pathname == '/daten-vorbereiten':
#         return data_preparation.layout
#     if pathname == '/verfahren-waehlen':
#         return method_lobby.layout
#     if pathname == '/diagramm-dashboard':
#         return chart_dashboard.layout
#     if pathname == '/interaktive-diagrame':
#         return interactive_charts.layout
#     if pathname == '/clustering':
#         return clustering.layout
#     if pathname == '/profiling':
#         return profiling.layout
#     #if pathname == '/prototyp':
#     #    return prototyp.layout
#     else: return error.layout




if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port='5000')