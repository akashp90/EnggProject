from datastore import db
from sqlalchemy import ForeignKey

class Diarrhea(db.Model):
    __tablename__="Diarrhea"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Diarrhea_Pred(db.Model):
    __tablename__="Diarrhea_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
   
class Gastroenteritis(db.Model):
    __tablename__="Gastroenteritis"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Gastroenteritis_Pred(db.Model):
    __tablename__="Gastroenteritis_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)

class Dengue(db.Model):
    __tablename__="Dengue"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Dengue_Pred(db.Model):
    __tablename__="Dengue_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
   
    
class Typhoid(db.Model):
    __tablename__="Typhoid"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Typhoid_Pred(db.Model):
    __tablename__="Typhoid_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Shigellosis(db.Model):
    __tablename__="Shigellosis"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Shigellosis_Pred(db.Model):
    __tablename__="Shigellosis_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,  ForeignKey('locations.id'), nullable=False)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
