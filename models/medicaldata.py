from datastore import db

class centreloc(db.Model):
    __tablename__='centreloc'
    CentreCode=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Location=db.Column(db.String(300))
    District=db.Column(db.String(300),nullable=False)
    State=db.Column(db.String(300))
    Country=db.Column(db.String(300))

class medicaldata(db.Model):
    __tablename__='medicaldata'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)

