from flask_restful import Resource
from flask import render_template, make_response, request, redirect, url_for
from wtforms import Form, StringField, IntegerField, TextAreaField, PasswordField, validators, SelectField
from passlib.hash import sha256_crypt
from models import PHCUser
from datastore import db

class RegisterForm(Form):
        name = StringField('Name', [validators.Length(min=1, max=50)])
        username = StringField('Username', [validators.Length(min=4, max = 25)])
        location = StringField('Centre Code (provided to you)', [validators.DataRequired()])
        password = PasswordField('Password', [validators.DataRequired(), 
            validators.EqualTo('confirm', 
            message = 'Passwords do not match')])
        confirm = PasswordField('Confirm Password')

class Register(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        form = RegisterForm(request.form)
        return make_response(render_template('register.html', form=form),200,headers)
    def post(self):
        form = RegisterForm(request.form)
        name = form.name.data
        location = form.location.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))
        phc_user = PHCUser(name=name, username=username, location=int(location), password=password)
        db.session.add(phc_user)
        db.session.commit()
        return redirect(url_for('login'))
        


