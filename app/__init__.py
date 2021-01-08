from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity, get_jwt_claims
from .utils import create_data
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()


def create_app(testing=False):

    app = Flask(__name__,instance_relative_config=False)
    app.config['JWT_SECRET_KEY']= "testingsecret"    
    jwt = JWTManager(app)

    from .views import auth
    from . import models

    """ 
    Create a function that will be called whenever 
    create_access_token is used. It will take whatever object is passed
    into the create_access_token method, and lets us define what custom
    claims should be added to the access token
    """
    @jwt.user_claims_loader
    def add_claims_to_access_token(user):
        return {
            'username' : user.username,
            'id':user.id
        }

    @jwt.user_identity_loader
    def user_identity_loader(user):
        return user.email

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
    
    @app.route('/jwt-test',methods=['GET'])
    @jwt_required
    def jwt_test():
        user_email = get_jwt_identity()
        user_id = get_jwt_claims()['id']
        user = models.Users.query.get(user_id)
        return jsonify({'message': user_email == user.email})

    with app.app_context():
        db.drop_all()
        db.create_all()

        create_data(db, models)
        return app
