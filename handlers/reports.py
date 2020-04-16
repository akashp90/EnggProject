from flask_restful import Resource
from flask import render_template, make_response, send_from_directory, redirect, request
from models import PHCUser,medicaldata,reports,centreloc
from datastore import db
from datetime import datetime
from handlers.generate_report import *
from handlers.generate_prediction import *

class Reports(Resource):
    def get(self):
        list_reports=reports.query.order_by(reports.ReportTime.desc()).all()
        print(list_reports)
        for i in list_reports:
            print(i,"\n",i.ReportLoc,i.ReportTime)
        list_rep=[]
        for i in list_reports:
            rep_name="Report as on "+i.ReportTime.strftime("%d %b %Y")
            tmp={ 'ReportTime':i.ReportTime.strftime("%d %b %Y %H:%M:%S"), 'ReportLoc':i.ReportLoc, 'ReportName':rep_name}
            list_rep.append(tmp)
        headers = {'Content-Type': 'text/html'}
        print(list_rep)
        return make_response(render_template('reports.html',reports=list_rep),200,headers)

class Output(Resource):
    def get(self,path):
        headers = {'Content-Type': 'text/html'}
        if("reports/" in path):
            print(path)
            return send_from_directory('',path)
        else:
            return make_response(render_template('error.html', errormsg="Access Denied"),200,headers)

class GenRep(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        generate_report()
        return make_response(render_template('error.html', errormsg="Access Denied"),200,headers)


def generate_report(algorithm=None,launch_method='auto'):    
    gen_pred(algorithm)
    gen_report(launch_method,algorithm)
