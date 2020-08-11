from flask import Flask
from datastore import db
from flask_restful import Api
from handlers import *
from models import *
from apscheduler.schedulers.background import BackgroundScheduler
from handlers.generate_prediction import *


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
    # Ensure FOREIGN KEY for sqlite3
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        def _fk_pragma_on_connect(dbapi_con, con_record):  # noqa
            dbapi_con.execute('pragma foreign_keys=ON')

        with app.app_context():
            from sqlalchemy import event
            event.listen(db.engine, 'connect', _fk_pragma_on_connect)


def _init_routes():
    api = Api(app)
    api.add_resource(Home, "/", methods=["GET"])
    api.add_resource(Login, "/login", methods=["GET", "POST"])
    api.add_resource(Register, "/register", methods=["GET", "POST"])
    api.add_resource(PHCDashboard, "/phcdashboard", methods=["GET"])
    api.add_resource(UploadCSV, "/uploadcsv", methods=["GET", "POST"])
    api.add_resource(Logout, "/logout", methods=["GET"])
    api.add_resource(Reports, "/reports", methods=["GET"])
    api.add_resource(Output, "/output/<path:path>", methods=["GET"])
    api.add_resource(GenRep, "/gen", methods=["GET"])  # Manual Report generation trigger
    # Generate report for non-default algorithms. Default is ARIMA
    api.add_resource(Algo, "/algo", methods=["GET"])
    api.add_resource(DownloadTemplate, "/download_template", methods=["GET", "POST"])
    api.add_resource(Admin, "/admin", methods=["GET", "POST"])
    api.add_resource(CoronavirusHandler, "/coronavirus", methods=["GET", "POST"])
    api.add_resource(About, "/about", methods=["GET"])
    api.add_resource(AdminLogin, "/admin_login", methods=["GET","POST"])


if __name__ == "__main__":
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(generate_report, trigger='cron', day_of_week='mon-sun', hour='0', minute='0')
    scheduler.add_job(train_all_models,trigger='cron',day_of_week='sun',hour='0' ,minute='0')
    scheduler.start()
    _init_routes()
    _init_db(app)
    app.run(debug=False,threaded=False)
