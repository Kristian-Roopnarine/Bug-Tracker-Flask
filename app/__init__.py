from flask import Flask


def create_app(testing_config=None):

    app = Flask(__name__)    
    
    from . import db
    from bug_tracker.views import auth
    
    db.init_app(app)
    app.register_blueprint(auth.bp)


    @app.route('/',methods=['GET'])
    def index():
        return 'App is running'



    return app
