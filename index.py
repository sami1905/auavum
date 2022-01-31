from app import app

# dash app
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
    


if __name__ == '__main__':
    app.run_server(debug=True)