from handlers.ml_algorithm_aditya import *
from handlers.ml_algorithms import *

def gen_pred(algorithm=None,launch_method='auto'):
    print("Prediction storage code goes here")
    if(algorithm=="LSTM"):
        LSTM_Aditya(launch_method)
    elif(algorithm=="ARIMA"):
        ARIMA_Likhith()
    else:
        pass
    print("Predictions generated and stored")
    
