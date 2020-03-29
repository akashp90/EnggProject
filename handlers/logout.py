from flask_restful import Resource
from flask import session, redirect, url_for


class Logout(Resource):
    def get(self):
        session.clear
        return redirect(url_for("login"))

