from flask_restful import Resource
from flask import make_response, render_template, Markup, request, current_app, redirect, url_for, flash, send_file
from datetime import date
import pandas as pd
from handlers.corona import get_moving_average_growth_rate_and_prediction
import os
from handlers.logged_in_required import login_required

class CoronavirusHandler(Resource):
    @login_required
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('corona_virus_report_template.html', reportdate=str(date.today()) ),200,headers)
        #return make_response(render_template('dashboard.html'),200,headers)
    @login_required
    def post(self):
        from handlers.corona import get_moving_average_growth_rate_and_prediction
        state_name = request.form.get('state_name')
        df = pd.read_csv('covid_19_india.csv')
        state_names = df['State/UnionTerritory'].values
        available_state_names = set(state_names)
        print("state_name =>", state_name)
        print("state names =>", state_names)
        if state_name not in available_state_names:
            error = "Invalid statename"
            headers = {'Content-Type': 'text/html'}
            flash(error, "danger")
            return redirect(url_for('admin'))
        else:
            root_path = current_app.root_path
            filename = 'static/' + str(date.today()) + '_00-00-00_' + 'coronavirus_Prediction_' + state_name+ '.png'
            if not os.path.exists(root_path+'/'+filename):
                print("Filename not found->", filename)
                print("Report generating for the first time")
                get_moving_average_growth_rate_and_prediction('covid_19_india.csv',state_name=state_name)
            
            
            headers = {'Content-Type': 'text/html'}
            return make_response(render_template('state_coronavirus_pred.html', filename=filename))



