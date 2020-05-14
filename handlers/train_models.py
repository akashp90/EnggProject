import numpy as np
from numpy import array
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from joblib import dump, load
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime,timedelta
from tensorflow.keras.models import load_model
from models import Diseases,algorithms,Location
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
import os
from datastore import db
from keras.metrics import Accuracy

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

def train_LSTM():
    list_diseases=Diseases.query.order_by(Diseases.Disease).all()
    for i in list_diseases:
        df=pd.read_sql("""SELECT EntryTime, sum(NoOfCases) as Count FROM """+i.Disease+""" GROUP BY EntryTime ORDER BY EntryTime;""",db.engine)
        raw_seq = np.ravel(df.iloc[:,1:2].values)
        raw_seq=raw_seq.reshape(len(raw_seq),1)
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaler = scaler.fit(raw_seq)
        raw_seq=scaler.transform(raw_seq)
        n_steps = 7
        X, y = split_sequence(raw_seq, n_steps)
        n_features = 1
        X = X.reshape((X.shape[0], X.shape[1], n_features))
        model = Sequential()
        model.add(LSTM(50, activation='relu', input_shape=(n_steps, n_features)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse',metrics=[Accuracy()])
        model.fit(X, y, epochs=200, verbose=0)
        fd=os.getcwd()+"/MLModels/LSTM_"+i.Disease+".tf"
        print(fd)
        model.save(fd)
        fd=os.getcwd()+"/MLModels/LSTM_"+i.Disease+"_Scaler.gz"
        print(fd)
        dump(scaler,fd)
        print("Training complete")
    

        