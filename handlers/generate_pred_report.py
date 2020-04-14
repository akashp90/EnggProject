import os
import numpy as np
import pandas as pd
from datetime import datetime
from models import reports
from datastore import db

def gen_pred(algorithm=None):
    print("Predictions generated and stored")
    #Generate new predictions and store them via this function - Probably Likhith

def gen_report(launch_method='auto',algorithm=None):
    dir=os.getcwd()
    if(launch_method=='auto'):
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
        filename="""\\reports\\"""+currtime.strftime("%Y-%m-%d_00-00-00")+".html"        
    else:
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d %H %M %S"),"%Y %m %d %H %M %S")
        filename="""\\reports\\"""+currtime.strftime("%Y-%m-%d_%H-%M-%S")+"_custom.html"
    str1="""<html><body><h1>Hello World!</h1></body></html>"""
    dir=dir+filename
    print(dir)
    try:
        fd=open(dir,'w')
        fd.write(str1)
        fd.close()
        if(algorithm==None):
            rep=reports(ReportTime=currtime,ReportLoc=filename)
        else:
            rep=reports(ReportTime=currtime,ReportLoc=filename,Algorithm=algorithm)
        db.session.add(rep)
        db.session.commit()
    except FileExistsError as e:
        print("File Exists",e)
    #Add report generation code
    print("Reports generated")
    #Add prediction table deletion code
    
    
