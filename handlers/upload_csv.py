from flask_restful import Resource
from flask import (
    make_response,
    render_template,
    redirect,
    request,
    flash,
    current_app,
    url_for,
)
from werkzeug.utils import secure_filename
import os
from handlers.dump_to_database import DumpToDatabase
import pandas as pd

ALLOWED_EXTENSIONS = {"csv"}
MANDATORY_COLUMN_NAMES = ["Date", "Disease", "Age"]


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    # Basically, see if the filename is allowed or not. That is, check if the part after
    # The . is a list in ALLOWED_EXTENSIONS. which just contains 'csv'


def validate_csv(file, filename, mandatory_column_names):
    df = pd.read_csv(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    column_names = df.columns.values
    if column_names.sort() == mandatory_column_names.sort():
        return True
    return False


class UploadCSV(Resource):
    def get(self):
        headers = {"Content-Type": "text/html"}
        return make_response(render_template("upload_csv.html"), 200, headers)

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
            if validate_csv(file, filename, MANDATORY_COLUMN_NAMES):
                DumpToDatabase.dump_to_database(
                    filename, table_name="medicaldata"
                )
                return redirect(url_for("phcdashboard"))
            else:
                flash("Column names in csv not correct", "danger")
                return redirect(request.url)

