from datastore import db

class Disease(db.Model):
	id = db.Column(db.Integer, primary_key= True,autoincrement=True)
	name = db.Column(db.String,nullable=False)
    
