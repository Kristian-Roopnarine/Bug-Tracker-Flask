from flask import (
    Blueprint, jsonify, g, flash, request, render_template
)
from werkzeug.exceptions import abort
from app.models import db, Users
import bcrypt


bp = Blueprint('auth',__name__,url_prefix='/auth')

def hash_password(passwd):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(passwd.encode('utf-8'),salt)

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
    user = db.session.execute(
        'SELECT email FROM users WHERE email = :email OR username = :username', {"email":email,"username":username}
    )
    if user.fetchone():
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
    """
    result = db.session.execute(
        'INSERT INTO users (email, username, password) VALUES (:email, :username, :password)', {"email":email,"username":username,"password":password}
    )
    print(result)
    db.session.commit()
    """
    # instead of returning user, return JWT token
    return jsonify({"user": user.serialize()})


# login user