from flask_restful import Resource
from flask import render_template, make_response
from models import Disease
from datastore import db

class DiseaseHandler(Resource):
	def get(self):
		headers = {'Content-Type': 'text/html'}
		disease = Disease(id=124, name='Malaria')
		db.session.add(disease)
		db.session.commit()

		return make_response(render_template('disease.html'), 200, headers)



