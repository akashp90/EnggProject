from flask_restful import Resource
from flask import render_template, make_response, request, session, flash, redirect, url_for
from models import PHCUser
from datastore import db
from passlib.hash import sha256_crypt

class Login(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'),200,headers)
    def post(self):
        username = request.form['username']
        password_candidate = request.form['password']  #This is the password the user has entered.
        phc_user = PHCUser.query.filter_by(username=username).first()
        
        if phc_user:
            password = phc_user.password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['username'] = username
                flash('You are now logged in!', 'success')
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template("dashboard.html"),200,headers)
            else:
                error = "Invalid credentials"
                headers = {'Content-Type': 'text/html'}
                return make_response(render_template("login.html", error=error),200,headers)

