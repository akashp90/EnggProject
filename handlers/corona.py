
import pandas as pd
import numpy as np
import datetime
import requests
import warnings

import matplotlib.pyplot as plt
import matplotlib
import matplotlib.dates as mdates

import squarify
import plotly.offline as py

from statsmodels.tsa.arima_model import ARIMA


from IPython.display import Image
import datetime


def get_table_in_html(input_filename):

    india_covid_19 = pd.read_csv(input_filename)#1st problem
    india_covid_19['Date'] = pd.to_datetime(india_covid_19['Date'],dayfirst = True)

    state_cases = india_covid_19.groupby('State/UnionTerritory')['Confirmed','Deaths','Cured'].max().reset_index()
    state_cases['Active'] = state_cases['Confirmed'] - (state_cases['Deaths']+state_cases['Cured'])
    state_cases["Death Rate (per 100)"] = np.round(100*state_cases["Deaths"]/state_cases["Confirmed"],2)
    state_cases["Cure Rate (per 100)"] = np.round(100*state_cases["Cured"]/state_cases["Confirmed"],2)
    state_table = (state_cases.sort_values('Confirmed', ascending= False).fillna(0)
    .style.background_gradient(cmap='Blues',subset=["Confirmed"])                        
    .background_gradient(cmap='Blues',subset=["Deaths"])                        
    .background_gradient(cmap='Blues',subset=["Cured"])                        
    .background_gradient(cmap='Blues',subset=["Active"])                        
    .background_gradient(cmap='Blues',subset=["Death Rate (per 100)"])                        
    .background_gradient(cmap='Blues',subset=["Cure Rate (per 100)"]))

    #TODO use state_table_html in rendering in admin page
    state_table_html = state_table.render()
    filename = 'coronavirus_reports/' + datetime.date.today().strftime("%Y-%m-%d") + '_00-00-00_' + 'coronavirus-table.html'
    with open(filename,'w') as file:
        file.write(state_table_html)
    filename = 'static/' + str(datetime.date.today()) + '_00-00-00_' + 'coronavirus-table.html'
    with open(filename,'w') as file:
        file.write(state_table_html)
    return


def calc_movingaverage(values ,N):    
    cumsum, moving_aves = [0], [0,0]
    for i, x in enumerate(values, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            moving_aves.append(moving_ave)
    return moving_aves

def calc_growthRate(values):
    k = []
    for i in range(1,len(values)):
        summ = 0
        for j in range(i):
            summ = summ + values[j]
        rate = (values[i]/summ)*100
        k.append(float(rate))
    return k


def get_moving_average_growth_rate_and_prediction(input_filename, state_name='Karnataka'):
    matplotlib.use('Agg')
    india_covid_19 = pd.read_csv(input_filename)#1st problem
    india_covid_19['Date'] = pd.to_datetime(india_covid_19['Date'],dayfirst = True)
    all_state = list(india_covid_19['State/UnionTerritory'].unique())
    all_state.remove('Unassigned')
    latest = india_covid_19[india_covid_19['Date'] > '30-01-20']
    state_cases = latest.groupby('State/UnionTerritory')['Confirmed','Deaths','Cured'].max().reset_index()
    latest['Active'] = latest['Confirmed'] - (latest['Deaths']- latest['Cured'])
    state_cases = state_cases.sort_values('Confirmed', ascending= False).fillna(0)
    states =list(state_cases['State/UnionTerritory'][0:15])

    states_confirmed = {}
    states_deaths = {}
    states_recovered = {}
    states_active = {}
    states_dates = {}

    for state in states:
        df = latest[latest['State/UnionTerritory'] == state].reset_index()
        k = []
        l = []
        m = []
        n = []
        for i in range(1,len(df)):
            k.append(df['Confirmed'][i]-df['Confirmed'][i-1])
            l.append(df['Deaths'][i]-df['Deaths'][i-1])
            m.append(df['Cured'][i]-df['Cured'][i-1])
            n.append(df['Active'][i]-df['Active'][i-1])
        states_confirmed[state] = k
        states_deaths[state] = l
        states_recovered[state] = m
        states_active[state] = n
        date = list(df['Date'])
        states_dates[state] = date[1:]
        


    fig = plt.figure(figsize= (25,17))

    plt.suptitle('5-Day Moving Average of Confirmed Cases in Top 15 States',fontsize = 20,y=1.0)
    k=0
    for i in range(1,15):
        ax = fig.add_subplot(5,3,i)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        ax.bar(states_dates[states[k]],states_confirmed[states[k]],label = 'Day wise Confirmed Cases ') 
        moving_aves = calc_movingaverage(states_confirmed[states[k]],5)
        ax.plot(states_dates[states[k]][:-2],moving_aves,color='red',label = 'Moving Average',linewidth =3)  
        plt.title(states[k],fontsize = 20)
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper left')
        k=k+1
    plt.tight_layout(pad=3.0)

    #First output
    moving_average_fig = fig
    filename = 'coronavirus_reports/' + datetime.date.today().strftime("%Y-%m-%d") + '_00-00-00_' + 'coronavirus-MovingAverageGraph.png'
    moving_average_fig.savefig(filename)
    filename = 'static/' + str(datetime.date.today()) + '_00-00-00_' + 'coronavirus-MovingAverageGraph.png'
    moving_average_fig.savefig(filename)

    fig = plt.figure(figsize= (25,17))
    plt.suptitle('Growth Rate in Top 15 States',fontsize = 20,y=1.0)
    k=0
    for i in range(1,15):
        ax = fig.add_subplot(5,3,i)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b'))
        #ax.bar(states_dates[states[k]],states_confirmed[states[k]],label = 'Day wise Confirmed Cases ') 
        growth_rate = calc_growthRate(states_confirmed[states[k]])
        ax.plot_date(states_dates[states[k]][21:],growth_rate[20:],color = '#9370db',label = 'Growth Rate',linewidth =3,linestyle='-')  
        plt.title(states[k],fontsize = 20)
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper left')
        k=k+1
    plt.tight_layout(pad=3.0)

    growth_rate_graph_fig = fig
    filename = 'coronavirus_reports/' + datetime.date.today().strftime("%Y-%m-%d") + '_00-00-00_' + 'coronavirus-GrowthRateGraph.png'
    growth_rate_graph_fig.savefig(filename)
    filename = 'static/' + str(datetime.date.today()) + '_00-00-00_' + 'coronavirus-GrowthRateGraph.png'
    growth_rate_graph_fig.savefig(filename)

    k = india_covid_19[india_covid_19['State/UnionTerritory']== state_name].iloc[:,[1,8]]

    data=k.values
    data=k

    arima = ARIMA(data['Confirmed'], order=(5, 1, 0))
    arima = arima.fit(trend='c', full_output=True, disp=True)
    forecast = arima.forecast(steps= 30)
    pred = list(forecast[0])

    start_date = data['Date'].max()
    prediction_dates = []
    for i in range(30):
        date = start_date + datetime.timedelta(days=1)
        prediction_dates.append(date)
        start_date = date
    fig = plt.figure(figsize= (15,10))
    plt.xlabel("Dates",fontsize = 20)
    plt.ylabel('Total cases',fontsize = 20)
    plt.title("Predicted Values for the next 15 Days for " +state_name , fontsize = 20)

    plt.plot_date(y= pred,x= prediction_dates,linestyle ='dashed',color = '#ff9999',label = 'Predicted');
    plt.plot_date(y=data['Confirmed'],x=data['Date'],linestyle = '-',color = 'blue',label = 'Actual');
    plt.legend()

    prediction_fig = fig

    filename = 'coronavirus_reports/' + str(datetime.date.today()) + '_00-00-00_' + 'coronavirus_Prediction_' + state_name +'.png'
    prediction_fig.savefig(filename)
    filename = 'static/' + str(datetime.date.today()) + '_00-00-00_' + 'coronavirus_Prediction_' + state_name+ '.png'
    prediction_fig.savefig(filename)

def get_results(filename='covid_19_india.csv'):
    get_moving_average_growth_rate_and_prediction(filename)
    get_table_in_html(filename)
