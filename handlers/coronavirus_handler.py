from flask_restful import Resource
from flask import make_response, render_template, Markup
from datetime import date

class CoronavirusHandler(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('corona_virus_report_template.html', reportdate=str(date.today()) ),200,headers)
        #return make_response(render_template('dashboard.html'),200,headers)

