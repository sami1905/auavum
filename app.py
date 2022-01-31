from flask import Flask
from dash_app import create_dash_app


app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Wartungsmodus!</h1><p>Auf der Website finden zur Zeit Wartungsarbeiten statt!Die Website ist deshalb bis auf weiteres nicht verfügbar.</p>"

create_dash_app(app)


if __name__ == "__main__":
    app.run(host='0.0.0.0')