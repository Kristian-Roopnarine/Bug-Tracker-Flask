from flask import (
    Blueprint, jsonify, g, flash, request, render_template
)
from werkzeug.exceptions import abort
from bug_tracker.db import get_pg_cursor_conn
import bcrypt


bp = Blueprint('auth',__name__,url_prefix='/auth')

def hash_password(passwd):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(passwd.encode('utf-8'),salt)

# sign up user
@bp.route('/register',methods=['GET','POST'])
def register():
    conn, cursor = get_pg_cursor_conn()
    # get email address
    email = request.json.get('email')
    # get username
    username = request.json.get('username')
    # get password
    password = request.json.get('password')
    # get password confirm
    password_confirm = request.json.get('password_confirm')   
    # check if user exists in DB 
    cursor.execute(
        'SELECT email FROM users WHERE email = %s OR username = %s', (email,username)
    )
    user = cursor.fetchone()
    if user:
        return jsonify({'message':'A user with that email address or username already exists.'})

    if password != password_confirm:
        return jsonify({'message':'The two passwords do not match'})
    
    password = hash_password(password)

    cursor.execute(
        'INSERT INTO users (email, username, password) VALUES (%s, %s, %s)', (email, username, password)
    )
    conn.commit()

    return jsonify({"message":"Created the user"})


# login user