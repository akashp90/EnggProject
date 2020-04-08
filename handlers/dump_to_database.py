import pandas as pd
from flask import current_app, session
import os
from models import medicaldata, PHCUser
from datastore import db
from datetime import datetime

class DumpToDatabase:
    @classmethod
    def dump_to_database(cls, filename, table_name):
        df = pd.read_csv(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
        if(session['username']):
            print(session['username'])
            user1=PHCUser.query.filter_by(username=session['username']).first()
            if user1:
                print(user1)
                userloc=user1.location
                print(userloc)
                if table_name == "medicaldata":
                    if ('Disease' == df.columns.values[1]) and ('Age' == df.columns.values[2]) and ('Date'==df.columns.values[0]):
                        if ('NoOfPatients' in df.columns.values) and ('NoOfPatients' == df.columns.values[3]):
                            vals=df.values
                            for i in vals:
                                temp=medicaldata(EntryTime=datetime.strptime(i[0],"%d/%m/%y %I:%M %p"),CentreCode=userloc,Disease=i[1],Age=i[2],NoOfCases=i[3])
                                print(temp)
                                db.session.add(temp)
                                db.session.commit()
                        else:
                            vals=df.values
                            for i in vals:
                                temp=medicaldata(EntryTime=datetime.strptime(i[0],"%d/%m/%y %I:%M %p"),CentreCode=userloc,Disease=i[1],Age=i[2])
                                print(temp)
                                db.session.add(temp)
                                db.session.commit()
                    else:
                        print("Invalid Format/Column Names. Use Date, Disease, Age, NoOfPatients as Column Names.")
            else:
                print("User Not logged in")

