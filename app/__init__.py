from flask import Flask
from app import routes


def create_app():
    app = Flask(__name__)

    # flask config
    # database
    # migrate
    routes.init_app(app)

    return app
