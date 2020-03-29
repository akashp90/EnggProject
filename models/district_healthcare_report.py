from datastore import db

class DistrictHealthcareReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String) #Should convert to a foreign key on Disease table
    no_of_patients = db.Column(db.String)
    date = db.Column(db.String)
    location = db.Column(db.String)

