from flask_restful import Resource
from flask import render_template, make_response
from models import reports

class Admin(Resource):
    def get(self):
        r=reports.query.order_by(reports.ReportTime.desc())
        lr=r[0].ReportTime
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('admin.html',lastreport=lr), 200, headers)
