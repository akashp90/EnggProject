from datastore import db
from sqlalchemy import ForeignKey

class PHCUser(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    username = db.Column(db.String)
    location = db.Column(db.Integer, ForeignKey('locations.id'), nullable=False)
    password = db.Column(db.String(100))
    permission = db.Column(db.String(10),default='User')
