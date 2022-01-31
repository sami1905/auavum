from flask import Flask
from dash_app import create_dash_app


app = Flask(__name__)

create_dash_app(app)
  


if __name__ == "__main__":
    app.run(host='0.0.0.0')