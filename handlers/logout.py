from flask_restful import Resource
from flask import session, redirect, url_for
from handlers.logged_in_required import login_required

class Logout(Resource):
    @login_required
    def get(self):
        session.clear
        session['logged_in'] = False
        session['username'] = ''
        session['permission'] = ''
        return redirect(url_for("login"))

