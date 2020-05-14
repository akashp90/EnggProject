from flask_restful import Resource
from flask import render_template, make_response
# from models import reports


class About(Resource):
    def get(self):
        # r=reports.query.order_by(reports.ReportTime.desc())
        # lr=r[0].ReportTime
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('about.html'), 200, headers)
