from flask import Flask
from datastore import db
from flask_restful import Api
from handlers import *
from models import *
from apscheduler.schedulers.background import BackgroundScheduler

def _init_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    app.secret_key = "secret123"
    return app

   
app = _init_app()



def _init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def _init_routes():
    api = Api(app)
    api.add_resource(Sample, "/sample", methods=["GET"])
    api.add_resource(Home, "/", methods=["GET"])
    api.add_resource(Login, "/login", methods=["GET", "POST"])
    api.add_resource(Register, "/register", methods=["GET", "POST"])
    api.add_resource(PHCDashboard, "/phcdashboard", methods=["GET"])
    api.add_resource(UploadCSV, "/uploadcsv", methods=["GET", "POST"])
    api.add_resource(Logout, "/logout", methods=["GET"])
    api.add_resource(Reports,"/reports",methods=["GET"])
    api.add_resource(Output,"/output/<path:path>",methods=["GET"])

   

if __name__ == "__main__":
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(generate_report, trigger='cron', day_of_week='sun', hour='0', minute='0')
    scheduler.start()
    _init_routes()
    _init_db(app)
    app.run(debug=True)
    


