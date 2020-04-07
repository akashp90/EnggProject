from flask_restful import Resource
from flask import render_template, make_response, send_from_directory, redirect, request

class Reports(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

class Output(Resource):
    def get(self,path):
        return send_from_directory('',path)
