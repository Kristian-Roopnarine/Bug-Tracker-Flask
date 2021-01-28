from flask import (
    Blueprint, jsonify, g, flash, request, render_template
)
from sqlalchemy import or_
from werkzeug.exceptions import abort
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, get_jwt_claims
)
from app.models import db, Users
import bcrypt


bp = Blueprint('auth',__name__,url_prefix='/auth')


# sign up user
@bp.route('/register',methods=['GET','POST'])
def register():
    # get email address
    email = request.json.get('email')
    # get username
    username = request.json.get('username')
    # get password
    password = request.json.get('password')
    # get password confirm
    password_confirm = request.json.get('password_confirm')   
    # check if user exists in DB 
    user = Users.query.filter(or_(Users.username==username,Users.email==email)).first()
    if user:
        return jsonify({'message':'A user with that email address or username already exists.'})

    if password != password_confirm:
        return jsonify({'message':'The two passwords do not match'})
    
    user = Users(
        email = email,
        username = username,
        password = password
    )
    db.session.add(user)
    db.session.commit()
    # instead of returning user, return JWT token
    access_token = create_access_token(identity=user)
    return jsonify({'access_token':access_token,"message":"Account created"})


# login user
@bp.route('/login',methods=['GET','POST'])
def login():
    # get email and password
    email = request.json.get('email')
    password = request.json.get('password')

    # check if user exists
    user = Users.query.filter_by(email=email).first()
    # if no user exists then return error
    if user is None:
        return jsonify({'message':'Invalid email or password'})
    """
    encoded_pass = password.encode('utf-8')
    user_pass = user.password.encode('utf-8')
    # compare password with hashed password
    """
    if user.is_password_correct(password):
        # return JWT token
        access_token = create_access_token(identity=user)
        return jsonify({'message':'Login success','access_token':access_token})

    # return error
    return jsonify({'message':'Invalid email or password'})
        