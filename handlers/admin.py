from flask_restful import Resource
from flask import render_template, make_response, session, request, redirect, url_for
from models import reports
from handlers.logged_in_required import login_required
from models import Location
from datastore import db

class Admin(Resource):
    @login_required
    def get(self):
        r=reports.query.order_by(reports.ReportTime.desc()).all()
        print(r)
        if(len(r)>0):
            lr=r[0].ReportTime
        else:
            lr="None"
        headers = {'Content-Type': 'text/html'}
        logged_in_user = session['username']
        return make_response(render_template('admin.html',username=logged_in_user), 200, headers)
    @login_required
    def post(self):
        district = request.form.get('district')
        country = request.form.get('country')
        state = request.form.get('state')
        cordinates = request.form.get('cord')
        location = Location(district=district, country=country, state=state, location_coord=cordinates)
        db.session.add(location)
        db.session.commit()
        flash("New location created. Use id ="+location.id+" to register", "success")
        return redirect(url_for('admin'))


