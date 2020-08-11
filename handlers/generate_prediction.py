from handlers.ml_algorithm_aditya import *
from handlers.ml_algorithms import *
from handlers.train_models import *

def gen_pred(algorithm=None,launch_method='auto'):
    print("Prediction storage code goes here")
    if(algorithm=="LSTM"):
        LSTM_Aditya(launch_method)
        MLP_Aditya(launch_method)
    elif(algorithm=="Coronavirus"):
        pass #Handled elsewhere
    else:
        pass
    print("Predictions generated and stored")
    
def train_all_models():
    train_LSTM()
