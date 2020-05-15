from flask_restful import Resource
from flask import (
    make_response,
    render_template,
    redirect,
    request,
    flash,
    current_app,
    url_for,
    session
)
from werkzeug.utils import secure_filename
import os
from handlers.dump_to_database import DumpToDatabase
from models import PHCUser, Location
import pandas as pd
import csv

ALLOWED_EXTENSIONS = {"csv"}

def get_mandatory_column_names_for_disease(disease):
    if disease == 'DIARRHEA':
        return ['EntryTime','Age', 'NoOfCases']
    return


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    # Basically, see if the filename is allowed or not. That is, check if the part after
    # The . is a list in ALLOWED_EXTENSIONS. which just contains 'csv'


def validate_csv(file, filename, mandatory_column_names):
    # TODO Validate filename, see if it is in the correct format that we need 
    df = pd.read_csv(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    column_names = df.columns.values
    if column_names.sort() == mandatory_column_names.sort():
        return True
    return False


class UploadCSV(Resource):
    def get(self):
        headers = {"Content-Type": "text/html"}
        username = session['username']
        phc_user = PHCUser.query.filter_by(username=username).first()
        location_id = phc_user.location
        location = Location.query.filter_by(id=location_id).first()
        district = location.district

        return make_response(render_template("upload_csv.html",location_id=location_id,district=district,username=username), 200, headers)

    def post(self):
        if "file" not in request.files:
            flash("No file part", "danger")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file", "danger")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            disease = filename.split('_')[0]
            mandatory_column_names = get_mandatory_column_names_for_disease(disease)
            if validate_csv(file, filename, mandatory_column_names):
                try:
                    DumpToDatabase.dump_to_database(
                        filename, table_name=disease
                    )
                    flash("Saved to db successfully", "success")
                except Exception as e:
                    print("Exception->", e)
                    flash("There was an error in saving to database, please check your file","danger")
                return redirect(url_for("phcdashboard"))
            else:
                flash("Column names in csv not correct", "danger")
                return redirect(request.url)

