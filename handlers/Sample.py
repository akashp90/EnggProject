from flask_restful import Resource
from models import Test12
from datastore import db
class Sample(Resource):
    def get(self):
        test = Test12(id=1, name="Hello")
        db.session.add(test)
        db.session.commit()
        return "Heheh"