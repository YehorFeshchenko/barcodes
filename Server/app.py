from flask import Flask
from flask_cors import CORS
from models import base
from routes.drugs import blueprint as drugs_blueprint
import logging
import datetime

db = base.db

date = datetime.datetime.now().date()

logging.basicConfig(filename=f'encoder_{date}.log',
                    encoding='utf-8',
                    level=logging.DEBUG)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)
    return app


app = create_app()

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(drugs_blueprint,  url_prefix='/drugs')

