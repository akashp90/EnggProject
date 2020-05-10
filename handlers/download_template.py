from flask_restful import Resource
from flask import render_template, make_response, send_file, request, flash
import csv
from models import Diarrhea
# TODO can make a radio button to choose the disease instead of user input

class DownloadTemplate(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('download_template.html'),200,headers)

    def post(self):
        disease_name = request.form['disease_name']
        column_names = []
        if disease_name == 'Diarrhea':
            column_names = Diarrhea.__table__.columns.keys()
            column_names.remove('id')
            column_names.remove('CentreCode')
        # TODO Add support for more diseases
        
        if len(column_names) == 0:
            error = "Disease not supported yet"
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template("download_template.html", error=error),200,headers)

        with open('template.csv','w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
        return send_file('template.csv', as_attachment=True, attachment_filename=disease_name.upper() + '_DD_MM_YYYY.csv')
