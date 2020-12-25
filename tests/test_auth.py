import json
import unittest
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

if __name__ == "__main__":
    unittest.main()