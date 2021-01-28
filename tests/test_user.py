import json
import unittest
from flask_jwt_extended import get_jwt_claims,get_jwt_identity
from app.models import Users,create_password_hash
from test_auth import loginUser, getJWT
from base import BaseCase


def changePassword(self, jwt, new_pass="1234", new_pass_confirm="1234"):
    return self.client.patch(
        '/user/password-reset',
        data=json.dumps(dict(
            password = new_pass,
            password_confirm = new_pass_confirm
            )
        ),
        headers = {
            'Authorization':'Bearer {}'.format(jwt)
        },
        content_type="application/json"
    )


class TestUserBlueprint(BaseCase):
    
    def test_user_password_change(self):
        pass

