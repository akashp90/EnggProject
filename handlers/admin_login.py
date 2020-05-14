from flask_restful import Resource
from models import AdminModel
from passlib.hash import sha256_crypt
from flask import make_response, render_template, session, flash, request, redirect, url_for
from datastore import db

class AdminLogin(Resource):
    def get(self):
        if not AdminModel.query.all():
            admin_model = AdminModel(name='admin',username='admin',password=sha256_crypt.encrypt('password'))
            db.session.add(admin_model)
            db.session.commit()

        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'),200,headers)
    def post(self):
        username = request.form['username']
        password_candidate = request.form['password']  #This is the password the user has entered.
        admin_user = AdminModel.query.filter_by(username=username).first()

        if admin_user:
            password = admin_user.password
            if sha256_crypt.verify(password_candidate,password):
                session['logged_in'] = True
                session['username'] = username
                session['permission'] = 'admin'
                flash('You are now logged in!', 'success')
                headers = {'Content-Type': 'text/html'}
                return redirect(url_for('admin'))
            else:
                error = "Invalid credentials"
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template("login.html", error=error),200,headers)
        else:
            error = "Admin not found"
            headers = {'Content-type': 'text/html'}
            return make_response(render_template('login.html', error=error), 200, headers)