from flask_testing import TestCase
import app
from app.models import db

class BaseCase(TestCase):
    
    def create_app(self):
        self.app = app.create_app(testing=True)
        self.app.config['TESTING'] = True
        self.app.config['DEBUG'] = False
        return self.app
    
    def setUp(self):
        db.drop_all()
        db.create_all()
        
        app.utils.create_data(db, app.models)

        
    
    def tearDown(self):
        pass