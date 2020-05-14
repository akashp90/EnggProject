from datastore import db

class AdminModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String(100))
    permission = db.Column(db.String(10),default='Admin')