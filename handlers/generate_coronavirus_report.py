from flask_restful import Resource
from flask import render_template, make_response, send_from_directory, redirect, request
from models import reports,algorithms
from datastore import db
from datetime import datetime
import os
def gen_coronavirus_report(launch_method,al):
    currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
    tx=render_template('corona_virus_report_template.html',reportdate=currtime.strftime("%Y-%m-%d_00-00-00"))
    filename = os.getcwd()+"""\\coronavirus_reports\\"""+currtime.strftime("%Y-%m-%d_00-00-00")+".html"
    filename1= """\\coronavirus_reports\\"""+currtime.strftime("%Y-%m-%d_00-00-00")+".html"
    try:
        fd=open(filename,'w')
        fd.write(tx)
        fd.close()
        if(al==None):
            rep=reports(ReportTime=currtime,ReportLoc=filename1)
        else:
            rep=reports(ReportTime=currtime,ReportLoc=filename1,Algorithm=al)
        db.session.add(rep)
        db.session.commit()
    except FileExistsError as e:
        print("File Exists",e)
    print("Reports generated")
