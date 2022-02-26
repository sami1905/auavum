import dash
import dash_bootstrap_components as dbc
from dash.long_callback import DiskcacheLongCallbackManager
import diskcache
cache = diskcache.Cache("./cache")
long_callback_manager = DiskcacheLongCallbackManager(cache)
from sent2vec.vectorizer import Vectorizer
vectorizer = Vectorizer()

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                ,long_callback_manager=long_callback_manager
                )
app.title = 'Auswertung und Analyse von Umfragen'


server = app.server