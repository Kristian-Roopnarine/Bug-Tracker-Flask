from flask import (
    Blueprint, jsonify, g, flash, request, render_template
)
from sqlalchemy import or_
from werkzeug.exceptions import abort
from app.models import db, Users
import bcrypt


bp = Blueprint('auth',__name__,url_prefix='/auth')

def hash_password(passwd):
    # this is probably taking long
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(passwd.encode('utf-8'),salt).decode('utf-8')

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
    """
    user = db.session.execute(
        'SELECT email FROM users WHERE email = :email OR username = :username', {"email":email,"username":username}
    )
    """
    if user:
        return jsonify({'message':'A user with that email address or username already exists.'})

    if password != password_confirm:
        return jsonify({'message':'The two passwords do not match'})
    
    password = hash_password(password)
    user = Users(
        email = email,
        username = username,
        password = password
    )
    db.session.add(user)
    db.session.commit()
    # instead of returning user, return JWT token
    return jsonify({"user": user.serialize()})


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
        return jsonify({'message':'Invalid username or password'})

    encoded_pass = password.encode('utf-8')
    user_pass = user.password.encode('utf-8')
    # compare password with hashed password

    if bcrypt.checkpw(encoded_pass, user_pass):
        # return JWT token
        return jsonify({'message':'Login success'})
        
    # return error
    return jsonify({'message':'Invalid password'})
        