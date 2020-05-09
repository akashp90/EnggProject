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

class predictions(db.Model):
    __tablename__='predictions'
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    Disease=db.Column(db.String(300),nullable=False) #Which disease prediction
    AgeGroup=db.Column(db.String(20),nullable=False) #Age groups = 1-20, 20-40, 40-60, 60-80, 80+
    CentreCode=db.Column(db.Integer,nullable=False)  #Centre code from centreloc table
    NoOfCases=db.Column(db.Integer,nullable=False)   #Predicted no.of cases for Disease and age group for centre
    Date=db.Column(db.DateTime)                      #Date/Start date of week for which prediction is made
    AlgorithmName = db.Column(db.String(100),nullable=False)
    
class Diarrhea(db.Model):
    __tablename__="Diarrhea"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Diarrhea_Pred(db.Model):
    __tablename__="Diarrhea_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Gastroenteritis(db.Model):
    __tablename__="Gastroenteritis"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Gastroenteritis_Pred(db.Model):
    __tablename__="Gastroenteritis_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)

class Typhoid(db.Model):
    __tablename__="Typhoid"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Typhoid_Pred(db.Model):
    __tablename__="Typhoid_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Shigellosis(db.Model):
    __tablename__="Shigellosis"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
class Shigellosis(db.Model):
    __tablename__="Shigellosis_Pred"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    EntryTime=db.Column(db.DateTime)
    CentreCode=db.Column(db.Integer,nullable=False)
    Disease=db.Column(db.String(300),nullable=False)
    Age=db.Column(db.Integer)
    NoOfCases=db.Column(db.Integer, default=1, nullable=False)
    
