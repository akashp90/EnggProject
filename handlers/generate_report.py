import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from models import reports
from datastore import db


def gen_report(launch_method='auto',algorithm=None):
    dir=os.getcwd()
    if(launch_method=='auto'):
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
        filename="""\\reports\\"""+currtime.strftime("%Y-%m-%d_00-00-00")+".html"        
    else:
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d %H %M %S"),"%Y %m %d %H %M %S")
        filename="""\\reports\\"""+currtime.strftime("%Y-%m-%d_%H-%M-%S")+"_custom.html"
    dir=dir+filename
    print(dir)
    