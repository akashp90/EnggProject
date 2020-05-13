from datastore import db
from sqlalchemy import ForeignKey

class medicaldata(db.Model):
    __tablename__='medicaldata'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)

class medicaldata_pred(db.Model):
    __tablename__='medicaldata_pred'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    EntryTime = db.Column(db.DateTime)
    CentreCode = db.Column(db.Integer,nullable=False)
    Disease = db.Column(db.String(300),nullable=False)
    Age = db.Column(db.Integer)
    NoOfCases = db.Column(db.Integer, default=1, nullable=False)

class reports(db.Model):
    __tablename__='reports'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    ReportTime=db.Column(db.DateTime,nullable=False)
    ReportLoc=db.Column(db.String(1000),nullable=False)
    Algorithm=db.Column(db.String(300))
    
class algorithms(db.Model):
    __tablename__='algorithms'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    AlgorithmName=db.Column(db.String(100),nullable=False)
    AlgorithmLoc = db.Column(db.String(1000),nullable=False)
    DefaultAlgorithm = db.Column(db.Boolean,nullable=False, default=False)
    Accuracy = db.Column(db.String(20))

class outbreak_analysis(db.Model):
    __tablename__='outbreak_analysis'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    EntryTime = db.Column(db.DateTime)
    CentreCode = db.Column(db.Integer)
    Disease = db.Column(db.String(200))
    OutbreakFlag = db.Column(db.Integer)