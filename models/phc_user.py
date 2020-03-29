from datastore import db

class PHCUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    location = db.Column(db.String)
    password = db.Column(db.String(100))
