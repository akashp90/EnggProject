import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime,timedelta
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from joblib import dump, load
from models import Diseases,algorithms,Location
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
    locations1 = Location.query.order_by(Location.id).all()
    diseases=[]
    queries=[]
    if(launch_method=='auto'):
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
    else:
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d %H %M %S"),"%Y %m %d %H %M %S")
    lastweek=currtime-timedelta(currtime.weekday())-timedelta(weeks=1)
    nextweek = currtime+timedelta(weeks=1,days=1)
    print(nextweek)
    for i in diseases1:
        diseases.append(i.Disease)
        model = load_model(algorithms1+"_"+i.Disease+".tf")
        for j in locations1:
            df=pd.read_sql("""SELECT EntryTime, CentreCode, sum(NoOfCases) as Count FROM """+i.Disease+""" WHERE EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND CentreCode="""+str(j.id)+""" GROUP BY EntryTime ORDER BY EntryTime DESC;""",db.engine)
            if(len(df.values)==0):
                print("None")
                continue
            else:
                df['EntryTime']=pd.to_datetime(df['EntryTime'])
                idx = pd.date_range(lastweek, currtime)
                df.index=pd.DatetimeIndex(df['EntryTime'])
                df = df.reindex(idx, fill_value=0)
                df=df.drop(labels='EntryTime',axis=1)
                df['CentreCode']=j.id
                print(df)
                preds=[]
                for k in range(0,7):
                    model_inputs=np.ravel(df.iloc[0:3,1:2].values)
                    print(model_inputs)
                    model_inputs=np.append(model_inputs,preds)
                    print(model_inputs)
                    model_inputs=model_inputs[-3:]
                    model_inputs=model_inputs.reshape(len(model_inputs),1)
                    scaler=MinMaxScaler(feature_range=(0,1))
                    scaler=scaler.fit(model_inputs)
                    model_inputs=scaler.transform(model_inputs)
                    model_inputs=model_inputs.reshape((1,3,1))
                    preds.append(np.round(model.predict(model_inputs),1))
                preds=np.ravel(preds)
                print(preds)
                
                idx = pd.date_range(currtime,nextweek)
                print(idx)
                for k in range(7):
                    db.engine.execute("""INSERT INTO """+i.Disease+"""_Pred (EntryTime, CentreCode, NoOfCases) VALUES('"""+str(idx[k])+"""',"""+str(j.id)+""","""+str(int(preds[k]))+""");""")
    print("In LSTM")
    
