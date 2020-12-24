from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .utils import create_data
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()


def create_app(testing=False):

    app = Flask(__name__,instance_relative_config=False)    
    
    from .views import auth
    from . import models

    if testing:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("TEST_DB")
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DEV_DB")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)    
    app.register_blueprint(auth.bp)

    @app.route('/',methods=['GET'])
    def index():
        return 'App is running'

    with app.app_context():
        db.drop_all()
        db.create_all()

        create_data(db, models)
        return app
