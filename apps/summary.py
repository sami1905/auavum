from dash.dependencies import Input, Output, State, ALL, ALLSMALLER, MATCH
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from app import app
from summarizer import Summarizer

summary_model= Summarizer()

def layout():
    children = dbc.Container([
            html.Div([], id='test'),    
            html.Button("Änder Test", id="btn_test", n_clicks=0)
        ])
    return children

@app.callback(Output("test", "children"), 
                [Input("btn_test", "n_clicks")]
)
def tab_content(btn):
    if btn:
        return html.P("BTN gedrückt")

    else:
        return html.P("Test")


def summarize(text):
    return summary_model(text, num_sentences=3)