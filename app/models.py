from . import db
import datetime
import bcrypt

class Users(db.Model):
    __tablename__= "users"
    
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    username = db.Column(db.String,unique=True,nullable=False)

    def __init__(self,email,password,username):
        self.username = username
        self.email = email
        self.password = self.hash_password(password)

    def is_password_correct(self, input_password):
        user_pass = self.password.encode('utf-8')
        encoded_pass = input_password.encode('utf-8')
        return bcrypt.checkpw(encoded_pass, user_pass)

    def hash_password(self, passwd):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(passwd.encode('utf-8'),salt).decode('utf-8')

    def __repr__(self):
        return f"""
            <User id={self.id} email={self.email} username={self.username} />
            """
    