from flask_restful import Resource
from flask import render_template, make_response, request, session, flash, redirect, url_for
from models import PHCUser,reports,Location
from datastore import db

class Admin(Resource):
    def get(self):
        r=reports.query.order_by(reports.ReportTime.desc()).all()
        print(r)
        if(len(r)>0):
            lr=r[0].ReportTime
        else:
            lr="None"
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('admin.html',lastreport=lr), 200, headers)
    def post(self):
        if('permissions' in session):
            if(session['permissions']=='Admin'):
                l = Location(district=request.form['district'], state=request.form['state'], country=request.form['country'], location_coord=request.form['cord'])
                db.session.add(l)
                db.session.commit()
                flash('Centre Added!', 'success')
            else:
                return make_response(render_template('admin.html',lastreport="None"), 200, {'Content-Type': 'text/html'})
        else:
            return make_response(render_template('admin.html',lastreport="None"), 200, {'Content-Type': 'text/html'})
