import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from joblib import dump, load
from models import Diseases,algorithms
from datastore import db

def split_sequence(sequence, n_steps):
	X, y = list(), list()
	for i in range(len(sequence)):
		# find the end of this pattern
		end_ix = i + n_steps
		# check if we are beyond the sequence
		if end_ix > len(sequence)-1:
			break
		# gather input and output parts of the pattern
		seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
		X.append(seq_x)
		y.append(seq_y)
	return array(X), array(y)

def LSTM_Aditya(launch_method):
    diseases1=Diseases.query.all()
    algorithms1=algorithms.query.filter_by(AlgorithmName="LSTM").first()
    algorithms1=algorithms1.AlgorithmLoc
    diseases=[]
    queries=[]
    if(launch_method=='auto'):
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
    else:
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d %H %M %S"),"%Y %m %d %H %M %S")
    lastweek=currtime-timedelta(currtime.weekday())-timedelta(weeks=1,days=1)
    for i in diseases1:
        diseases.append(i.Disease)
        model = load_model(algorithms1+"_"+i.Disease+".tf")
        df=pd.read_sql("""SELECT EntryTime, CentreCode, sum(NoOfCases) as Count FROM """+i.Disease+""" WHERE EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY CentreCode ORDER BY EntryTime DESC, CentreCode;""",db.engine)
        print(df.values)
        
    print("In LSTM")
    
def MLP_Aditya():
    #Add model loading based on disease
    clf = load('MLModels/MLP_Diarrhea.joblib')
    features=[44,44,44,45,45,45,45,47,48,49,50,54,55,56,57,57,56,57,57,58]
    labels=[0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    pred=clf.predict(features)
    print(pred)
    #Add pred to db
    print("In MLP")