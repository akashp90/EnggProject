import pandas as pd
import numpy as np
import sqlite3

df=pd.read_csv('Data4.csv')
df2=pd.read_csv('Ages.csv')
num = df2._get_numeric_data().values
nan_ar=np.isnan(num)
nnan_ar=~nan_ar
num=num[nnan_ar]
m=0
queries=[]
disease=['Gastroenteritis','Typhoid','Diarrhea','Shigellosis']
dfv=df.values
for i in range(0,len(dfv)):
    temp=[]
    for j in range(0,len(dfv[i]),2):
        temp.append(dfv[i][j])
    qr="""INSERT INTO medicaldata(EntryTime,CentreCode,Disease,Age) VALUES ('"""+str(temp[0])+"""',15,'"""
    for j in range(1,len(temp)):
        qr1=qr+disease[j-1]+"""',"""
        for k in range(0,temp[j]):
            qr2=qr1+str(int(num[m]))+""");"""
            m+=1
            queries.append(qr2)

conn=sqlite3.connect('test1.db')
for i in queries:
    print(conn.execute(i))

            
        