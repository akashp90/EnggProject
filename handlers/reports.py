from flask_restful import Resource
from flask import render_template, make_response, send_from_directory, redirect, request, Markup, render_template_string
from models import PHCUser,medicaldata,reports,algorithms
from datastore import db
from datetime import datetime
from handlers.generate_report import *
from handlers.generate_prediction import *
from handlers.generate_coronavirus_report import *

from handlers.corona import *
from handlers.generate_coronavirus_report import *

class Reports(Resource):
    def get(self):
        algo=request.args.get('algo',default=None,type=str)
        print(algo)
        if(algo!=None):
            list_reports=reports.query.filter_by(Algorithm=algo).order_by(reports.ReportTime.desc()).all()
        else:
            list_reports=reports.query.order_by(reports.ReportTime.desc()).all()
        print(list_reports)
        for i in list_reports:
            print(i,"\n",i.ReportLoc,i.ReportTime)
        list_rep=[]
        for i in list_reports:
            rep_name="Report as on "+i.ReportTime.strftime("%d %b %Y")
            tmp={ 'ReportTime':i.ReportTime.strftime("%d %b %Y %H:%M:%S"), 'ReportLoc':i.ReportLoc, 'ReportName':rep_name, 'AlgorithmName': i.Algorithm}
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
        elif("coronavirus_reports/" in path):
            return send_from_directory('',path)
        else:
            return make_response(render_template('error.html', errormsg="Access Denied"),200,headers)

class GenRep(Resource):
    def get(self):
        algo=request.args.get('algo',default=None,type=str)
        print(algo)
        headers = {'Content-Type': 'text/html'}
        if(algo!=None):
            generate_report(algo,'custom')
        else:
            generate_report()
        return make_response(redirect('/reports'),303,headers)

class Algo(Resource):
    def get(self):
        list_algorithms=algorithms.query.order_by(algorithms.DefaultAlgorithm.desc(),algorithms.AlgorithmName.asc()).all()
        alist=[]
        for i in list_algorithms:
            if(i.AlgorithmName!="MLP"):
                alist.append(i)
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('commanderconsole.html',algolist=alist),200,headers)

def generate_report(algorithm=None,launch_method='auto'): 
    if(algorithm=="Coronavirus"):
        get_results()
        gen_coronavirus_report(launch_method,algorithm)
        return
    if (algorithm==None):
        al=algorithms.query.filter_by(DefaultAlgorithm=True).first()
        al=al.AlgorithmName
    else:
        al=algorithm
    al1=algorithms.query.all()
    flag=0
    for i in al1:
        if(i.AlgorithmName==al):
            flag=1
    if(flag==0):
        raise Exception("Algorithm does not exist")
        
    gen_pred(al,launch_method)
    gen_report(launch_method,al)    
    
    get_results()
    gen_coronavirus_report(launch_method,algorithm)





