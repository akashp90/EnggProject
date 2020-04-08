import pandas as pd
from flask import current_app
import os
from models import medicaldata
from datastore import db


class DumpToDatabase:
    @classmethod
    def dump_to_database(cls, filename, table_name):
        df = pd.read_csv(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        print("Failed")
        
        if table_name == "null":
            for i in range(0, len(df)):
                row = df.iloc[i, :]
                disease = row["disease"]
                no_of_patients = str(row["no_of_patients"])
                date = row["date"]
                location = row["location"]
                district_healthcare_report = DistrictHealthcareReport(
                    disease=disease,
                    no_of_patients=str(no_of_patients),
                    date=date,
                    location=location,
                )
                print("Before committing")
                db.session.add(district_healthcare_report)
                db.session.commit()

