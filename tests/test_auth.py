import json
import unittest
from flask_jwt_extended import get_jwt_claims,get_jwt_identity
from app.models import Users

from base import BaseCase

def createUser(self):
    return self.client.post('/auth/register', data=json.dumps(
        dict(
            email="bob2@gmail.com",
            username="isnotkris_test",
            password="123",
            password_confirm="123"
        )
    ), content_type="application/json")

def passwordMismatch(self):
    return self.client.post('/auth/register', data=json.dumps(
        dict(
            email="bob2@gmail.com",
            username="isnotkris_test",
            password="123",
            password_confirm="12"
        )
    ), content_type="application/json")

def loginUser(self, email="bob@gmail.com",password="123"):
    return self.client.post('/auth/login',data=json.dumps(
        dict(
            email=email,
            password=password
        )
    ),content_type="application/json")

def getJWT(self):
    response = loginUser(self)
    data = json.loads(response.data.decode())
    return data['access_token']

def jwt_test_route(self, token):
    return self.client.get('/jwt-test',headers={
        'Authorization':'Bearer {}'.format(token)
    },content_type="application/json")

class TestAuthBlueprint(BaseCase):

    def test_register_unique_user(self):
        response = createUser(self)
        user = Users.query.get("2")
        self.assertEqual(user.email,"bob2@gmail.com")
        self.assertEqual(user.username,"isnotkris_test")
    
    def test_register_user_exists(self):
        createUser(self)
        response = createUser(self)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],'A user with that email address or username already exists.')
    
    def test_register_password_mismatch(self):
        response = passwordMismatch(self)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],'The two passwords do not match')
    
    def test_login_success(self):
        response = loginUser(self)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],'Login success')
    
    def test_login_fail_incorrect_email(self):
        response = loginUser(self,email="asdfasdf@gmail.com")
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],"Invalid email or password")
    
    def test_login_fail_incorrect_password(self):
        response = loginUser(self,password="12")
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],"Invalid email or password")
    
    def test_protected_route_with_token(self):
        token = getJWT(self)
        response = jwt_test_route(self, token)
        data = json.loads(response.data.decode())
        self.assertEqual(data['message'],True)

if __name__ == "__main__":
    unittest.main()