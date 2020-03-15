from flask import Flask
from datastore import db
from flask_restful import Api
from handlers import Sample
from models import *

def _init_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    return app
app = _init_app()

def _init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()



def _init_routes():
    api = Api(app)
    api.add_resource(Sample,'/sample',methods=['GET'])


if __name__=='__main__':
    _init_routes()
    _init_db(app)
    app.run(debug=True)


