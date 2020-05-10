#Likhith's ML models go here
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from datetime import datetime
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf, pacf 

def test_stationarity(timeseries):    
    ts_log = np.log(ts)
    rolmean = timeseries.rolling(window=24).mean() # 24 hours on each day
    rolstd = timeseries.rolling(window=24).std()
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    print ('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)

def ARIMA_Likhith():
    data = pd.read_csv('AirPassengers.csv')
    con=data['Month']
    data['Month']=pd.to_datetime(data['Month'])
    data.set_index('Month', inplace=True)
    ts = data['#cases']
    ts_log = np.log(ts)
    test_stationarity(ts)
    moving_avg =rolmean.rolling(window=12,center=False).mean()
    ts_log_moving_avg_diff = ts_log - moving_avg
    ts_log_moving_avg_diff.dropna(inplace=True)
    test_stationarity(ts_log_moving_avg_diff)
    expwighted_avg = ts_log.ewm(halflife=12,ignore_na=False,min_periods=0,adjust=True).mean()
    ts_log_ewma_diff = ts_log - expwighted_avg
    test_stationarity(ts_log_ewma_diff)
    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.isnull().sum() 
    ts_log_diff.dropna(inplace=True)
    test_stationarity(ts_log_diff)
    decomposition = seasonal_decompose(ts_log)
    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid
    ts_log_decompose = residual
    ts_log_decompose.dropna(inplace=True)
    test_stationarity(ts_log_decompose)
    lag_acf = acf(ts_log_diff, nlags=12)
    lag_pacf = pacf(ts_log_diff, nlags=12, method='ols')
    model=ARIMA(ts_log,order=(2 , 1, 0))
    results_AR=model.fit(disp=-1)
    predictions_ARIMA_diff=pd.Series(results_ARIMA.fittedvalues,copy=True)
    print (predictions_ARIMA_diff.head())
    predictions_ARIMA_diff_cumsum=predictions_ARIMA_diff.cumsum()
    print( predictions_ARIMA_diff_cumsum.head())
    predictions_ARIMA_log=pd.Series(ts_log.iloc[0],index=ts_log.index)
    predictions_ARIMA_log=predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
    predictions_ARIMA_log.head()
    predictions_ARIMA=np.exp(predictions_ARIMA_log)
    print("ARIMA Model")