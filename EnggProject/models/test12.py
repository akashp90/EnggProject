
from datastore import db

class Test12(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)