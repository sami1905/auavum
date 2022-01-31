from app import app
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

if __name__ == '__main__':
    app.run_server(debug=True)