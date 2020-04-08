from flask_restful import Resource
from flask import render_template, make_response, send_from_directory, redirect, request
from models import PHCUser,medicaldata,reports,centreloc
from datastore import db
from datetime import datetime

class Reports(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('index.html'),200,headers)

class Output(Resource):
    def get(self,path):
        headers = {'Content-Type': 'text/html'}
        if("reports/" in path):
            print(path)
            return send_from_directory('',path)
        else:
            return make_response(render_template('error.html', errormsg="Access Denied"),200,headers)
        
