from flask import Flask
from LinksShorter import app as _app
from LinksShorter.config import Config

config = Config()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config.database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(_app.app_index, url_prefix='/')
    return app
