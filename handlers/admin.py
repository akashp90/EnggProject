from flask_restful import Resource
from flask import render_template, make_response


class Admin(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('admin.html'), 200, headers)
    """def post(self):
        #TODO save to DB"""
