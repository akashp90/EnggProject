from datastore import db

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    location_name = db.Column(db.String())  #Coordinates
    district = db.Column(db.String(300),nullable=False)
    state=db.Column(db.String(300))
    country=db.Column(db.String(300))