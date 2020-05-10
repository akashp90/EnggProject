from datastore import db

class Diseases(db.Model):
    __tablename__='diseases'
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    Disease = db.Column(db.String(300),nullable=False)
    
