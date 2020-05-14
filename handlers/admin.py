from flask_restful import Resource
from flask import render_template, make_response
from models import reports

class Admin(Resource):
    def get(self):
        r=reports.query.order_by(reports.ReportTime.desc()).all()
        print(r)
        if(len(r)>0):
            lr=r[0].ReportTime
        else:
            lr="None"
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('admin.html'), 200, headers)
    """def post(self):
        #TODO save to DB"""
