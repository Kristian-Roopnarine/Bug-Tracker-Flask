from . import db
import datetime

class Users(db.Model):
    __tablename__= "users"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String,unique=True,nullable=False)
    password = db.Column(db.String,nullable=False)
    username = db.Column(db.String,unique=True,nullable=False)

    def __repr__(self):
        return f"""
            <User id={self.id} email={self.email} username={self.username} />
            """
    
    def serialize(self):
        return {
            "email":self.email,
            "username":self.username
        }