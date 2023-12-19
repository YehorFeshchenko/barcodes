import os
import datetime
import logging
from flask import Flask
from flask_cors import CORS
from models.base import db
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Initialize the database with the app
    db.init_app(app)

    # Setup CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app

if __name__ == "__main__":
    app = create_app()

    # Import and register blueprints after app creation
    from routes.components import blueprint as components_blueprint
    app.register_blueprint(components_blueprint, url_prefix='/components')

    # Configure logging
    date = datetime.datetime.now().date()
    logging.basicConfig(filename=f'logs/encoder_{date}.log', encoding='utf-8', level=logging.DEBUG)

    # Run the app within an application context
    with app.app_context():
        app.run(debug=True, port=8080)
