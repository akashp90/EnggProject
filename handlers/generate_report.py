import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from models import reports,algorithms
from datastore import db


def gen_report(launch_method='auto',al=None):
    dir=os.getcwd()
    if(launch_method=='auto'):
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
        filename="""/reports/"""+currtime.strftime("%Y-%m-%d_00-00-00")+".html"
    else:
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d %H %M %S"),"%Y %m %d %H %M %S")
        filename="""/reports/"""+currtime.strftime("%Y-%m-%d_%H-%M-%S")+"_custom.html"
    dir=dir+filename
    print(dir)
    #delete and recombine databases
    db.engine.execute("""DELETE FROM medicaldata;""")
    db.engine.execute("""DELETE FROM medicaldata_pred;""")
    disdf=pd.read_sql("""SELECT Disease FROM diseases;""",db.engine)
    for i in disdf.values:
        db.engine.execute("""INSERT INTO medicaldata(EntryTime,CentreCode,Disease,Age,NoOfCases) SELECT EntryTime,CentreCode, '"""+i[0]+"""' as Disease, Age,NoOfCases FROM """+i[0]+""";""")
        db.engine.execute("""INSERT INTO medicaldata_pred(EntryTime,CentreCode,Disease,NoOfCases) SELECT EntryTime,CentreCode,'"""+i[0]+"""' as Disease,NoOfCases FROM """+i[0]+"""_Pred;""")
   
    
    #data loading
    lastweek=currtime-timedelta(currtime.weekday())-timedelta(weeks=1,days=1)
    lastweek=datetime.strptime(lastweek.strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
    print("Lastweek:",lastweek)
    df=pd.read_sql("""SELECT Disease, sum(NoOfCases) as Count from medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Disease ORDER BY sum(NoOfCases) DESC""",db.engine)
    df2=pd.read_sql("""SELECT c.district as District, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, locations c WHERE m.CentreCode=c.id AND m.EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY c.district, m.Disease ORDER BY c.district, m.Disease""",db.engine)
    df3=pd.read_sql("""SELECT Age, count(Age)*NoOfCases as Count FROM medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Age ORDER BY Age""",db.engine)
    df4=pd.read_sql("""SELECT sum(NoOfCases) as Count FROM medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""'""",db.engine)
    last4wk=currtime-timedelta(currtime.weekday())-timedelta(weeks=4,days=1)
    last4wkstartdt=[]
    for i in range(0,4):
        last4wkstartdt.append(last4wk+timedelta(weeks=i))
    df5=pd.read_sql("""SELECT STRFTIME("%Y-%m-%d",EntryTime) as ETime, Disease, sum(NoOfCases) as Count FROM medicaldata WHERE  EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+last4wk.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY ETime,Disease ORDER BY ETime, Disease""",db.engine)
    df6=pd.read_sql("""SELECT STRFTIME("%Y-%m-%d",m.EntryTime) as ETime, c.district as District, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, locations c WHERE m.CentreCode=c.id AND m.EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND m.EntryTime>='"""+last4wk.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY ETime, c.district, m.Disease ORDER BY ETime, c.district, m.Disease""",db.engine)
    lastwkstart=lastweek-timedelta(weeks=1)
    df7=pd.read_sql("""SELECT sum(NoOfCases) as Count FROM medicaldata WHERE EntryTime<='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastwkstart.strftime("%Y-%m-%d %H:%M:%S")+"""'""",db.engine)
    df81 = pd.read_sql("""SELECT Disease, sum(NoOfCases) as OCount FROM medicaldata WHERE EntryTime<='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastwkstart.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Disease ORDER BY Disease;""",db.engine)
    df82 = pd.read_sql("""SELECT Disease, sum(NoOfCases) as NCount FROM medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Disease ORDER BY Disease;""",db.engine)
    df83 = pd.read_sql("""SELECT Disease FROM diseases ORDER BY Disease;""",db.engine)
    df8diffs={}
    for i in df83['Disease']:
        tempdiff=0
        print("df81",df81.values)
        for j in range(0,len(df81.values)-1):
            if(df81.values[j][0]==i):
                tempdiff=df81.values[j][1]
                break
        for j in range(len(df82.values)):
            if(df82.values[j][0]==i):
                if(tempdiff!=0):
                    tempdiff=((tempdiff-df82.values[j][1])*100)/tempdiff
                else:
                    tempdiff=df82.values[j][1]*100
                break
        df8diffs[i]=-tempdiff
    df8diffs = dict(sorted(df8diffs.items(), key = lambda kv:(kv[1], kv[0])))
    df8x=list(df8diffs.keys())
    df9 = pd.read_sql("""SELECT Disease, sum(NoOfCases) as Count FROM medicaldata_pred WHERE EntryTime>'"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Disease ORDER BY Count DESC;""",db.engine)
    df10 = pd.read_sql("""SELECT sum(NoOfCases) as Count FROM medicaldata_pred WHERE EntryTime>'"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""';""",db.engine)
    df11 = pd.read_sql("""SELECT c.district as District, m.Disease as Disease, sum(m.NoOfCases) as Count FROM medicaldata_pred m, locations c WHERE m.CentreCode=c.id AND m.EntryTime>'"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY m.CentreCode,m.Disease ORDER BY c.District;""",db.engine)
    currtime2=lastweek-timedelta(weeks=2)
    df121=pd.read_sql("""SELECT STRFTIME("%Y-%m-%d",EntryTime) as ETime, Disease, sum(NoOfCases) as Count FROM medicaldata WHERE  EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+currtime2.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY ETime,Disease ORDER BY ETime, Disease""",db.engine)
    df12 = pd.read_sql("""SELECT STRFTIME("%Y-%m-%d",EntryTime) as ETime, Disease, sum(NoOfCases) as Count FROM medicaldata_pred WHERE EntryTime>'"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY ETime,Disease ORDER BY ETime, Disease;""",db.engine)
    df12 = pd.concat([df121,df12],ignore_index=True)
    df13 = pd.read_sql("""SELECT c.district as District, sum(m.NoOfCases) as Count FROM medicaldata_pred m, locations c WHERE m.CentreCode=c.id AND EntryTime>'"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY m.CentreCode ORDER BY Count DESC;""",db.engine)
    outbreakalerttext=""
    df14=pd.read_sql("""SELECT c.district as Region, m.Disease, m.OutbreakFlag FROM outbreak_analysis m, locations c WHERE m.EntryTime>="""+currtime.strftime("%Y-%m-%d")+""" AND m.CentreCode=c.id ORDER BY Region;""",db.engine)
    print("Outbreak",df14)
    df14vals={}
    print(np.unique(df14['Region'].values),np.unique(df14['Disease'].values))
    for i in np.unique(df14['Region'].values):
        temp={}
        for j in np.unique(df14['Disease'].values):
            temp[j]=0        
        df14vals[i]=temp
    print(df14vals)
    for i in df14.values:
        if(i[2]>0):
            df14vals[i[0]][i[1]]+=1
    print(df14vals)
    for i in df14vals:
        for j in df14vals[i]:
            print(i,j)
            if(df14vals[i][j]>6):
                outbreakalerttext+=i+"-"+j+"; "
        
    
    pred_regmostcase = df13['District'].values[0]
    pred_regleastcase = df13['District'].values[-1]
    pred_dismostinfec = df9['Disease'].values[0]
    pred_changeincaseperc = ((df10.values[0][0]-df7.values[0][0])*100)/df7.values[0][0]
    pred_changeincaseperc = np.round(pred_changeincaseperc,2)
    if(pred_changeincaseperc>=0):
        pred_changeincase="+"+str(pred_changeincaseperc)+"(+"+str(df10.values[0][0]-df7.values[0][0])+" cases)"
    else:
        pred_changeincase = str(pred_changeincaseperc)+"("+str(df10.values[0][0]-df7.values[0][0])+" cases)"
    df9diffs1={}
    for i in df83['Disease']:
        tempdiff=0
        for j in range(len(df82.values)-1):
            if(df81.values[j][0]==i):
                tempdiff=df82.values[j][1]
                break
        for j in range(len(df9.values)):
            if(df9.values[j][0]==i):
                if(tempdiff!=0):
                    tempdiff=((tempdiff-df9.values[j][1])*100)/tempdiff
                else:
                    tempdiff=df9.values[j][1]*100
                break
        df9diffs1[i]=-tempdiff
    df9diffs1 = dict(sorted(df9diffs1.items(), key = lambda kv:(kv[1], kv[0])))
    df9x=list(df8diffs.keys())
    pred_dismostimpro = df9x[0]
    pred_disleastimpro = df9x[-1]
    predticks=[]
    for i in range(2,7):
        predticks.append(last4wk+timedelta(weeks=i))
    
    changeinwk=((df4.values[0][0]-df7.values[0][0])*100)/df7.values[0][0]
    changeinwk2=df4.values[0][0]-df7.values[0][0]
    changeinwk = round(changeinwk,2)
    if(changeinwk>0):
        changeinwk='+'+str(changeinwk)
    else:
        changeinwk=str(changeinwk)
    if(changeinwk2>0):
        changeinwk2='+'+str(changeinwk2)
    else:
        changeinwk2=str(changeinwk2)
    agecount=[0,0,0,0,0]
    for i in df3.values:
        if(i[0]>=0 and i[0]<=20):
            agecount[0]+=i[1]
        elif(i[0]>=21 and i[0]<=40):
            agecount[1]+=i[1]
        elif(i[0]>=41 and i[0]<=60):
            agecount[2]+=i[1]
        elif(i[0]>=61 and i[0]<=80):
            agecount[3]+=i[1]
        elif(i[0]>=81 and i[0]<200):
            agecount[4]+=i[1]
    maxagecount=agecount[0]
    maxagerange='0 - 20'
    for i in range(len(agecount)):
        if(agecount[i]>=maxagecount):
            maxagecount=agecount[i]
            if(i==0):
                maxagerange='0 yr - 20 yrs'
            elif(i==1):
                maxagerange='20 yrs - 40 yrs'
            elif(i==2):
                maxagerange='40 yrs - 60 yrs'
            elif(i==3):
                maxagerange='60 yrs - 80 yrs'
            else:
                maxagerange='80+ yrs'
    print(agecount)
    agecountperc=[]
    for i in agecount:
        agecountperc.append(round((i*100)/(df4.values[0][0]),1))
    #TODO Sort out statistics section and make predictions
    df8=pd.read_sql("""SELECT c.district as District, sum(m.NoOfCases) as Count FROM locations c, medicaldata m WHERE m.CentreCode=c.id AND m.EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY m.CentreCode ORDER BY Count DESC""",db.engine)
    str1="""<!DOCTYPE html>
            <html>
            <head>
            </head>
            <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/css/bootstrap-select.min.css">
            <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.14/dist/js/bootstrap-select.min.js"></script>
            <title>Disease Report - """+currtime.strftime("%d-%m-%Y %H:%M")+"""</title>
            </head>
            <body>
            <nav class="navbar navbar-expand-lg navbar-light bg-light">
                <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>
                <span class="navbar-brand">PandemicDetect</span>
                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                        <li class="nav-item active" id='report_nav_item' onclick="document.getElementById('report_content_div').style.display='block';document.getElementById('prediction_content_div').style.display='none';document.getElementById('report_nav_item').classList.add('active'); document.getElementById('pred_nav_item').classList.remove('active');">
                            <a class="nav-link" href="#blocked">Reports<span class="sr-only">(current)</span></a>
                        </li>
                        <li class="nav-item" id='pred_nav_item' onclick="document.getElementById('report_content_div').style.display='none';document.getElementById('prediction_content_div').style.display='block';document.getElementById('pred_nav_item').classList.add('active'); document.getElementById('report_nav_item').classList.remove('active');">
                            <a class="nav-link" href="#blocked">Predictions</a>
                        </li>
                    </ul>
                </div>
            </nav>
            <div id='prediction_content_div' style='width:100%; display:none;margin-top:5px;'>
                <h5 style='margin-left:10px;'>Report Generated at: """+currtime.strftime("%d-%m-%Y %H:%M")+"""</h5>
                <div style='margin-left:15px; margin-right:15px; margin-bottom:10px; border:2px solid #CFCFCF; padding:4px; border-radius:6px;'>
                        <h3>Predictions:</h3>
                        <div class='row' style='margin:5px; margin-left:15px;'>
                        <div class='col-lg-6'>
                        1. Number of new cases predicted: """+str(df10.values[0][0])+""" cases <br/>
                        2. Change in cases from last week: """+pred_changeincase+"""<br/>
                        3. Most infectious disease: """+pred_dismostinfec+""" <br/>
                        4. Disease showing most improvement: """+pred_dismostimpro+"""<br/>
                        5. Disease showing least improvement: """+pred_disleastimpro+"""<br/>
                        </div>
                        <div class='col-lg-6'>"""
    str1+="""           6. Prediction Algorithm used: """+al+"""<br/>
                        7. Region with highest cases this week: """+pred_regmostcase+""" <br/>
                        8. Region with least cases this week: """+pred_regleastcase+"""<br/>
                        9. Outbreak Alert: """+outbreakalerttext+"""<br/>
                        </div>
                        </div>
                </div>
                <div class='row' style='margin-bottom:10px; margin-left:15px; margin-right:15px; padding:4px; border: 2px solid #CFCFCF; border-radius:6px;'>
                    <div class='col-md-6'>
                        <div id='pred_disease_distribution_table' style='margin-left:5px; width:100%; min-height:300px; display:inline-block;'></div>
                    </div>
                    <div class='col-md-6'>
                        <div id='pred_disease_distribution_chart' style='min-height:300px; width:95%; display:inline-block;'></div>
                    </div>
                </div>
                <div style='margin-left:15px; margin-right:15px; margin-bottom:10px; padding:4px; border:2px solid #CFCFCF; border-radius:4px;'>
                    <div id='pred_centrewise_top10_dist_chart' style='margin:0px; height:400px; width:85%;'></div>
                    <div id='pred_centrewise_top10_dist_table' style='margin:0px; margin-left:15px; width:85%;'></div>
                </div>
                
                <div id='pred_4week_trendline' style='margin-bottom:10px; margin-left:15px; margin-right:15px;  height:400px; padding:4px; border:2px solid #CFCFCF; border-radius:4px;'></div>
                
                <div id='pred_centrewise_all_dashboard' style='margin-bottom:10px; margin-left:15px; margin-right:15px; padding:4px; border:2px solid #CFCFCF; border-radius:4px;'>
                            <div id='pred_centrewise_all_dist_filter' style='margin-left:8px;margin-top:10px;'></div>
                            <div id='pred_centrewise_all_dist_timefilter' style='margin-left:8px;'></div>
                            <select class="selectpicker" multiple data-live-search="true" id='pred_centrewise_all_dist_diseasefilter' data-none-selected-text='Filter by Diseases' style='margin-left:8px;'></select>
                            <div id='pred_centrewise_all_dist_chart' style='height:400px;'></div>
                </div>
                            
            </div>
            
            <div id='report_content_div' style='width:100%;margin-top:5px;'>
                <h5 style='margin-left:10px;'>Report Generated at: """+currtime.strftime("%d-%m-%Y %H:%M")+"""</h5>
                <div style='margin-left:15px; margin-right:15px; margin-bottom:10px; border:2px solid #CFCFCF; padding:4px; border-radius:6px;'>
                        <h3>Useful Stats:</h3>
                        <div class='row' style='margin:5px; margin-left:15px;'>
                        <div class='col-lg-6'>
                        1. Number of new cases this week: """+str(df4.values[0][0])+""" cases <br/>
                        2. Change in cases from last week: """+changeinwk+"""% ("""+changeinwk2+""" cases)<br/>
                        3. Most infectious disease: """+df.values[0][0]+""" <br/>
                        4. Most infected age group: """+maxagerange+"""<br/>
                        5. Disease showing most improvement from last week: """+df8x[0]+"""<br/>                      
                        </div>
                        <div class='col-lg-6'>
                        6. Disease showing least improvement from last week: """+df8x[-1]+"""<br/>
                        7. Region with highest cases this week: """+df8.values[0][0]+""" <br/>
                        8. Region with least cases this week: """+df8.values[-1][0]+"""<br/>
                        </div>
                        </div>
                </div>
                        <div class='row' style='margin-bottom:10px; margin-left:15px; margin-right:15px; padding:4px; border:2px solid #CFCFCF; border-radius:6px;'>
                        <div class='col-md-6'>
                            <div id='age_distribution_table' style='margin-left:5px; width:100%; height:300px; display:inline-block;'></div>
                        </div>
                        <div class='col-md-6'>
                            <div id='age_distribution_chart' style='height:300px; width:95%; display:inline-block;'></div>
                        </div>
                        </div>
                        <div class='row' style='margin-bottom:10px; margin-left:15px; margin-right:15px; padding:4px; border: 2px solid #CFCFCF; border-radius:6px;'>
                        <div class='col-md-6'>
                            <div id='disease_distribution_table' style='margin-left:5px; width:100%; min-height:300px; display:inline-block;'></div>
                        </div>
                        <div class='col-md-6'>
                            <div id='disease_distribution_chart' style='min-height:300px; width:95%; display:inline-block;'></div>
                        </div>
                        </div>
                        
                        <div style='margin-left:15px; margin-right:15px; margin-bottom:10px; padding:4px; border:2px solid #CFCFCF; border-radius:4px;'>
                        <div id='centrewise_top10_dist_chart' style='margin:0px; height:400px; width:85%;'></div>
                        <div id='centrewise_top10_dist_table' style='margin:0px; margin-left:15px; width:85%;'></div>
                        </div>
                        
                        <div id='4week_trendline' style='margin-bottom:10px; margin-left:15px; margin-right:15px;  height:400px; padding:4px; border:2px solid #CFCFCF; border-radius:4px;'></div>
                        
                        <div id='centrewise_all_dashboard' style='margin-bottom:10px; margin-left:15px; margin-right:15px; padding:4px; border:2px solid #CFCFCF; border-radius:4px;'>
                            <div id='centrewise_all_dist_filter' style='margin-left:8px;margin-top:10px;'></div>
                            <div id='centrewise_all_dist_timefilter' style='margin-left:8px;'></div>
                            <select class="selectpicker" multiple data-live-search="true" id='centrewise_all_dist_diseasefilter' data-none-selected-text='Filter by Diseases' style='margin-left:8px;'></select>
                            <div id='centrewise_all_dist_chart' style='height:400px;'></div>
                        </div>
                        
                    </div>
                    
            </div>"""
    
    #Javascript section
    str1+="""<script type='text/javascript'>
                document.getElementById('prediction_content_div').style.display='block';
                google.charts.load('current', {packages:['corechart','table','annotatedtimeline','bar','annotatedtimeline','controls']});
                google.charts.setOnLoadCallback(drawChart);
                console.log("In the Script");
                
                function drawChart(){
                    console.log("In DrawChart");
                    //Charts Objects
                    var age_distribution_chart = new google.visualization.PieChart(document.getElementById('age_distribution_chart'));
                    var age_distribution_table = new google.visualization.Table(document.getElementById('age_distribution_table'));
                    var disease_distribution_table = new google.visualization.Table(document.getElementById('disease_distribution_table'));
                    var disease_distribution_chart = new google.visualization.PieChart(document.getElementById('disease_distribution_chart'));
                    var centrewise_top10_dist_table = new google.visualization.Table(document.getElementById('centrewise_top10_dist_table'));
                    var centrewise_top10_dist_chart = new google.visualization.BarChart(document.getElementById('centrewise_top10_dist_chart'));
                    var x4week_trendline = new google.visualization.LineChart(document.getElementById('4week_trendline'));
                    var centrewise_all_dashboard = new google.visualization.Dashboard(document.getElementById('centrewise_all_dashboard'));
                    var centrewise_all_dist_filter = new google.visualization.ControlWrapper({'controlType':'CategoryFilter', 'containerId':'centrewise_all_dist_filter','options':{'filterColumnLabel':'District','ui':{'allowTyping':false,'allowMultiple':false,'allowNone':false}}});

                    
                    var pred_disease_distribution_table = new google.visualization.Table(document.getElementById('pred_disease_distribution_table'));
                    var pred_disease_distribution_chart = new google.visualization.PieChart(document.getElementById('pred_disease_distribution_chart'));  var pred_centrewise_top10_dist_table = new google.visualization.Table(document.getElementById('pred_centrewise_top10_dist_table'));
                    var pred_centrewise_top10_dist_chart = new google.visualization.BarChart(document.getElementById('pred_centrewise_top10_dist_chart'));
                    var pred_x4week_trendline = new google.visualization.LineChart(document.getElementById('pred_4week_trendline'));
                    var pred_centrewise_all_dashboard = new google.visualization.Dashboard(document.getElementById('pred_centrewise_all_dashboard'));
                    
                
                    //data for charts
                    var age_distribution_data = new google.visualization.DataTable();
                    age_distribution_data.addColumn('string','Age Group (years)');
                    age_distribution_data.addColumn('number','No. of Cases');
                    age_distribution_data.addColumn('number','Percentage (%)');"""

    str1+="""       age_distribution_data.addRow(['0 - 20',"""+str(agecount[0])+""","""+str(agecountperc[0])+"""]);
                    age_distribution_data.addRow(['20 - 40',"""+str(agecount[1])+""","""+str(agecountperc[1])+"""]);
                    age_distribution_data.addRow(['40 - 60',"""+str(agecount[2])+""","""+str(agecountperc[2])+"""]);
                    age_distribution_data.addRow(['60 - 80',"""+str(agecount[3])+""","""+str(agecountperc[3])+"""]);
                    age_distribution_data.addRow(['80+',"""+str(agecount[4])+""","""+str(agecountperc[4])+"""]);  
                    age_distribution_chart.draw(age_distribution_data,{height:'90%',width:'90%',title:'Age Group Distribution (Current Week)',titleTextStyle:{color: 'black', fontName: 'Arial', fontSize: 16}});       
                    age_distribution_table.draw(age_distribution_data,{width: '80%', height: '75%'});
                    
                    var disease_distribution_data = new google.visualization.DataTable();
                    disease_distribution_data.addColumn('string','Disease');
                    disease_distribution_data.addColumn('number','No. of Cases');
                    disease_distribution_data.addColumn('number','Percentage (%)');"""
    for i in df.values:
        str1+="""disease_distribution_data.addRow(['"""+i[0]+"""',"""+str(i[1])+""","""+str(round((i[1]*100)/(df4.values[0][0]),1))+"""]);"""
    str1+="""disease_distribution_table.draw(disease_distribution_data,{width: '80%', height: '90%',page:'enable',pageSize:15});
            disease_distribution_chart.draw(disease_distribution_data,{height:'90%',width:'90%',title:'Disease Distribution (Current Week)',titleTextStyle:{color: 'black', fontName: 'Arial', fontSize: 16}});"""
    df2=df2.pivot(index='District',columns='Disease')
    df2=df2.fillna(0)
    df2['Sum']=df2.sum(axis=1)
    df2=df2.sort_values(by=['Sum'],ascending=False).head(10)
    df2=df2.drop(labels='Sum', axis=1)
    df2=df2.reindex(df2.sum().sort_values(ascending=False).index, axis=1)
    df2=df2.iloc[:,0:10]
    
    str1+="""   var centrewise_top10_dist_data = new google.visualization.DataTable();
                centrewise_top10_dist_data.addColumn('string','Region');"""
    for i in df2.columns.values:
        str1+="""centrewise_top10_dist_data.addColumn('number','"""+i[1]+"""');"""
    for i in range(len(df2.index.values)):
        str1+="""centrewise_top10_dist_data.addRow(['"""+df2.index.values[i]+"""'"""
        for j in df2.values[i]:
            str1+=','+str(j)
        str1+="""]);"""
    str1+="""centrewise_top10_dist_table.draw(centrewise_top10_dist_data,{width: '95%', height: '90%',page:'enable',pageSize:15});
            centrewise_top10_dist_chart.draw(centrewise_top10_dist_data,google.charts.Bar.convertOptions({isStacked:true,legend:{position:'right'},hAxis:{title:'No. of Cases'},title:'Top 10 Diseases Distribution for Top 10 Regions',fontSize:12,titleTextStyle:{color: 'black', fontName: 'Arial', fontSize: 16}}));
            
            var x4week_trendline_data = new google.visualization.DataTable();
            x4week_trendline_data.addColumn('date','Date');"""
    df5=df5.pivot(index='ETime',columns='Disease')
    df5=df5.fillna(0)
    df5=df5.reindex(df5.sum().sort_values(ascending=False).index, axis=1)
    df5=df5.iloc[:,0:10]
    
    for i in df5.columns.values:
        str1+="""x4week_trendline_data.addColumn('number','"""+i[1]+"""');"""
    for i in range(len(df5.index.values)):
        str1+="""x4week_trendline_data.addRow([new Date('"""+str(df5.index.values[i])+"""T00:00:00+05:30')"""
        for j in df5.values[i]:
            str1+=""","""+str(j)
        str1+="""]);"""
    str1+="""x4week_trendline.draw(x4week_trendline_data,{title:'Trends for Top 10 Diseases (Last 4 weeks)',height:'100%',width:'100%',legend:{position:'right'},height:350,fontSize:12,titleTextStyle:{color: 'black', fontName: 'Roboto', fontSize: 16},vAxis:{title:'New Cases per Day'},hAxis:{title:'Date',ticks:[new Date('"""+str(last4wkstartdt[0])+"""'),new Date('"""+str(last4wkstartdt[1])+"""'),new Date('"""+str(last4wkstartdt[2])+"""'),new Date('"""+str(last4wkstartdt[3])+"""'),new Date('"""+currtime.strftime('%Y-%m-%dT00:00:00+05:30')+"""')]}});"""
    
    last8wk=currtime-timedelta(currtime.weekday())-timedelta(weeks=8,days=1)
    last8wkdt=[]
    td=currtime-last8wk
    for i in range(0,td.days):
        last8wkdt.append(last8wk+timedelta(days=i))
    
    dfmain=pd.DataFrame()
    
    for i in range(len(last8wkdt)):
        df6=pd.read_sql("""SELECT c.district as District, STRFTIME("%Y-%m-%d",m.EntryTime) as ETime, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, locations c WHERE m.CentreCode=c.id AND ETime='"""+last8wkdt[i].strftime("%Y-%m-%d")+"""' GROUP BY c.district, m.Disease ORDER BY c.district, m.Disease""",db.engine)
        df6=df6.drop('ETime',axis=1)
        df6=df6.pivot(index='District',columns='Disease')
        df6=df6.fillna(0)
        dates=[]
        for j in range(df6.shape[0]):
            dates.append(last8wkdt[i].strftime("%Y-%m-%d"))
        df6.insert(loc=len(df6.columns),column='ETime',value=dates)
        dfmain=pd.concat([dfmain,df6])
        dfmain=dfmain.fillna(0)    
        
    str1+="""   var centrewise_all_dashboard_data = new google.visualization.DataTable();
                centrewise_all_dashboard_data.addColumn('date','Date');
                centrewise_all_dashboard_data.addColumn('string','District');"""
    for i in range(0,len(dfmain.columns)-1):
        str1+="""centrewise_all_dashboard_data.addColumn('number','"""+dfmain.columns[i][1]+"""');"""
    for i in range(len(dfmain.values)):
        str1+="""centrewise_all_dashboard_data.addRow([new Date('"""+str(dfmain.values[i][-1])+"""T00:00:00+05:30'),'"""+str(dfmain.index[i])+"""'"""
        for j in range(0,len(dfmain.values[i])-1):
            str1+=""","""+str(round(dfmain.values[i][j],0))
        str1+="""]);"""
    print(dfmain)
    str1+="""var centrewise_all_dist_chart = new google.visualization.ChartWrapper({'chartType':'LineChart','containerId':'centrewise_all_dist_chart','options':{'title':'Disease Trends By Region (max. past 8 weeks)','fontSize':'10','titleTextStyle':{'color':'black','fontName':'Arial','fontSize':'16','bold':'true','italic':'false'},'hAxis':{'title':'Date'},'vAxis':{'title':'New Cases per Day'},'width':'100%','height':'400px'},'view':{'columns':[0"""
    for i in range(len(dfmain.columns)-1):
        str1+=""","""+str(i+2)
    str1+="""]}});
    var centrewise_all_dist_filter = new google.visualization.ControlWrapper({'controlType':'CategoryFilter', 'containerId':'centrewise_all_dist_filter','options':{'filterColumnLabel':'District','ui':{'allowTyping':false,'allowMultiple':false,'allowNone':false,'label':'Choose a Region'}}});


    function changeColumnsViewed(e, clickedIndex, isSelected, previousValue){
        console.log($('#centrewise_all_dist_diseasefilter').selectpicker('val'));
        console.log(centrewise_all_dashboard_data);
        console.log(centrewise_all_dist_chart.getView());
        selectedValues=$('#centrewise_all_dist_diseasefilter').selectpicker('val');
        showViewArray=[0];
        for(var i=2; i<centrewise_all_dashboard_data.getNumberOfColumns();i++){
            if(selectedValues.length==0){
                    showViewArray.push(i);
            }
            else if(selectedValues.includes(centrewise_all_dashboard_data.getColumnLabel(i))){
                showViewArray.push(i);
            }
        }
        console.log(showViewArray);
        centrewise_all_dist_chart.setView({columns:showViewArray});
        centrewise_all_dist_chart.draw();
        console.log("Draw");
    }
    document.getElementById("centrewise_all_dist_diseasefilter").innerHTML = '"""
    for i in range(0,len(dfmain.columns)-1):
        str1+="""<option>"""+dfmain.columns[i][1]+"""</option>"""
    str1+="""';
    $('#centrewise_all_dist_diseasefilter').selectpicker('refresh');
    $('#centrewise_all_dist_diseasefilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
            changeColumnsViewed(e, clickedIndex, isSelected, previousValue);
    });

    var centrewise_all_dist_timefilter = new google.visualization.ControlWrapper({'controlType':'DateRangeFilter', 'containerId':'centrewise_all_dist_timefilter','options':{'filterColumnLabel':'Date','ui':{'label':'Choose a Time Frame'}}});
    centrewise_all_dashboard.bind([centrewise_all_dist_filter,centrewise_all_dist_timefilter],centrewise_all_dist_chart);
    centrewise_all_dashboard.draw(centrewise_all_dashboard_data);
    
    
    var pred_disease_distribution_data = new google.visualization.DataTable();
    var pred_centrewise_top10_dist_data = new google.visualization.DataTable();
    var pred_x4week_data = new google.visualization.DataTable();
    
    pred_disease_distribution_data.addColumn('string','Disease');
    pred_disease_distribution_data.addColumn('number','No. of Cases');
    pred_disease_distribution_data.addColumn('number','Percentage (%)');"""
    for i in df9.values:
        str1+="""pred_disease_distribution_data.addRow(['"""+i[0]+"""',"""+str(i[1])+""","""+str(round((i[1]*100)/(df10.values[0][0]),1))+"""]);"""
    str1+="""pred_disease_distribution_table.draw(pred_disease_distribution_data,{width: '80%', height: '90%',page:'enable',pageSize:15});
            pred_disease_distribution_chart.draw(pred_disease_distribution_data,{height:'90%',width:'90%',title:'Disease Distribution (Upcoming Week)',titleTextStyle:{color: 'black', fontName: 'Arial', fontSize: 16}});"""
    df11=df11.pivot(index='District',columns='Disease')
    df11=df11.fillna(0)
    df11['Sum']=df11.sum(axis=1)
    df11=df11.sort_values(by=['Sum'],ascending=False).head(10)
    df11=df11.drop(labels='Sum', axis=1)
    df11=df11.reindex(df11.sum().sort_values(ascending=False).index, axis=1)
    df11=df11.iloc[:,0:10]
    
    str1+="""pred_centrewise_top10_dist_data.addColumn('string','Region');"""
    for i in df11.columns.values:
        str1+="""pred_centrewise_top10_dist_data.addColumn('number','"""+i[1]+"""');"""
    for i in range(len(df11.index.values)):
        str1+="""pred_centrewise_top10_dist_data.addRow(['"""+df11.index.values[i]+"""'"""
        for j in df11.values[i]:
            str1+=','+str(j)
        str1+="""]);"""
    str1+="""pred_centrewise_top10_dist_table.draw(pred_centrewise_top10_dist_data,{width: '95%', height: '90%', page:'enable', pageSize:15});
            pred_centrewise_top10_dist_chart.draw(pred_centrewise_top10_dist_data,google.charts.Bar.convertOptions({isStacked:true,legend:{position:'right'},hAxis:{title:'No. of Cases'},title:'Predicted Top 10 Diseases Distribution for Top 10 Regions',fontSize:12,titleTextStyle:{color: 'black', fontName: 'Arial', fontSize: 16}}));
            pred_x4week_data.addColumn('date','Date'); """
    print(df12)
    df12=df12.pivot(index='ETime',columns='Disease')
    df12=df12.fillna(0)
    df12=df12.reindex(df12.sum().sort_values(ascending=False).index, axis=1)
    df12=df12.iloc[:,0:10]
    
    for i in df12.columns.values:
        str1+="""pred_x4week_data.addColumn('number','"""+i[1]+"""');"""
    for i in range(len(df12.index.values)):
        str1+="""pred_x4week_data.addRow([new Date('"""+str(df12.index.values[i])+"""T00:00:00+05:30')"""
        for j in df12.values[i]:
            str1+=""","""+str(j)
        str1+="""]);"""
    last2wkto2wk = []
    for i in range(0,5):
        dttemp=currtime2+timedelta(weeks=i)
        last2wkto2wk.append(dttemp.strftime("%Y-%m-%dT00:00:00+05:30"))
    str1+="""pred_x4week_trendline.draw(pred_x4week_data,{title:'Trends for Top 10 Diseases (Last 3 weeks to next 1 week)',height:'100%',width:'100%',legend:{position:'right'},fontSize:12,titleTextStyle:{color: 'black', fontName: 'Roboto', fontSize: 16},vAxis:{title:'New Cases per Day'},hAxis:{title:'Date', ticks:[new Date('"""+df12.index.values[0]+"""T00:00:00+05:30'),new Date('"""+last2wkto2wk[1]+"""'),new Date('"""+last2wkto2wk[2]+"""'),new Date('"""+last2wkto2wk[3]+"""'),new Date('"""+currtime.strftime("%Y-%m-%dT00:00:00+05:30")+"""'),new Date('"""+df12.index.values[len(df12.index.values)-1]+"""T00:00:00+05:30')]}});"""
    
    
    
    
    last7wk=currtime-timedelta(currtime.weekday())-timedelta(weeks=7,days=1)
    currtime3=currtime-timedelta(currtime.weekday())
    last7wkdt=[]
    for i in range(0,49):
        last7wkdt.append(last7wk+timedelta(days=i))
    #next1wk = currtime3+timedelta(weeks=1)-timedelta(days=1)
    next1wkdt=[]
    for i in range(0,7):
        next1wkdt.append(currtime3+timedelta(days=i))
    pred_dfmain=pd.DataFrame()
    
    for i in range(len(last7wkdt)):
        pred_df6=pd.read_sql("""SELECT c.district as District, STRFTIME("%Y-%m-%d",m.EntryTime) as ETime, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, locations c WHERE m.CentreCode=c.id AND ETime='"""+last7wkdt[i].strftime("%Y-%m-%d")+"""' GROUP BY c.district, m.Disease ORDER BY c.district, m.Disease""",db.engine)
        pred_df6=pred_df6.drop('ETime',axis=1)
        pred_df6=pred_df6.pivot(index='District',columns='Disease')
        pred_df6=pred_df6.fillna(0)
        dates_pred=[]
        for j in range(pred_df6.shape[0]):
            dates_pred.append(last7wkdt[i].strftime("%Y-%m-%d"))
        pred_df6.insert(loc=len(pred_df6.columns),column='ETime',value=dates_pred)
        pred_dfmain=pd.concat([pred_dfmain,pred_df6])
        pred_dfmain=pred_dfmain.fillna(0)   
    for i in range(len(next1wkdt)):
        pred_df15=pd.read_sql("""SELECT c.district as District, STRFTIME("%Y-%m-%d",m.EntryTime) as ETime, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata_pred m, locations c WHERE m.CentreCode=c.id AND ETime='"""+next1wkdt[i].strftime("%Y-%m-%d")+"""' GROUP BY c.district, m.Disease ORDER BY c.district, m.Disease;""",db.engine)
        pred_df15 = pred_df15.drop('ETime',axis=1)
        pred_df15 = pred_df15.pivot(index='District',columns='Disease')
        pred_df15 = pred_df15.fillna(0)
        dates_pred=[]
        for j in range(pred_df15.shape[0]):
            dates_pred.append(next1wkdt[i].strftime("%Y-%m-%d"))
        pred_df15.insert(loc=len(pred_df15.columns),column='ETime',value=dates_pred)
        pred_dfmain=pd.concat([pred_dfmain,pred_df15])
        pred_dfmain=pred_dfmain.fillna(0)
        
    print(pred_dfmain)
    str1+="""   var pred_centrewise_all_dashboard_data = new google.visualization.DataTable();
                pred_centrewise_all_dashboard_data.addColumn('date','Date');
                pred_centrewise_all_dashboard_data.addColumn('string','District');"""
    for i in range(0,len(pred_dfmain.columns)-1):
        str1+="""pred_centrewise_all_dashboard_data.addColumn('number','"""+pred_dfmain.columns[i][1]+"""');"""
    for i in range(len(pred_dfmain.values)):
        str1+="""pred_centrewise_all_dashboard_data.addRow([new Date('"""+str(pred_dfmain.values[i][-1])+"""T00:00:00+05:30'),'"""+str(pred_dfmain.index[i])+"""'"""
        for j in range(0,len(pred_dfmain.values[i])-1):
            str1+=""","""+str(round(pred_dfmain.values[i][j],0))
        str1+="""]);"""
    str1+="""var pred_centrewise_all_dist_chart = new google.visualization.ChartWrapper({'chartType':'LineChart','containerId':'pred_centrewise_all_dist_chart','options':{'title':'Predicted Disease Trends By Region (max. past 8 weeks to next 1 week)','fontSize':'10','titleTextStyle':{'color':'black','fontName':'Arial','fontSize':'16','bold':'true','italic':'false'},'hAxis':{'title':'Date'},'vAxis':{'title':'New Cases per Day'},'width':'100%','height':'400px'},'view':{'columns':[0"""
    for i in range(len(pred_dfmain.columns)-1):
        str1+=""","""+str(i+2)
    str1+="""]}});
    var pred_centrewise_all_dist_filter = new google.visualization.ControlWrapper({'controlType':'CategoryFilter', 'containerId':'pred_centrewise_all_dist_filter','options':{'filterColumnLabel':'District','ui':{'allowTyping':false,'allowMultiple':false,'allowNone':false,'label':'Choose a Region'}}});


    function pred_changeColumnsViewed(e, clickedIndex, isSelected, previousValue){
        selectedValues=$('#pred_centrewise_all_dist_diseasefilter').selectpicker('val');
        showViewArray=[0];
        for(var i=2; i<pred_centrewise_all_dashboard_data.getNumberOfColumns();i++){
            if(selectedValues.length==0){
                    showViewArray.push(i);
            }
            else if(selectedValues.includes(pred_centrewise_all_dashboard_data.getColumnLabel(i))){
                showViewArray.push(i);
            }
        }
        console.log(showViewArray);
        pred_centrewise_all_dist_chart.setView({columns:showViewArray});
        pred_centrewise_all_dist_chart.draw();
        console.log("Draw");
    }
    document.getElementById("pred_centrewise_all_dist_diseasefilter").innerHTML = '"""
    for i in range(0,len(pred_dfmain.columns)-1):
        str1+="""<option>"""+pred_dfmain.columns[i][1]+"""</option>"""
    str1+="""';
    $('#pred_centrewise_all_dist_diseasefilter').selectpicker('refresh');
    $('#pred_centrewise_all_dist_diseasefilter').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
            pred_changeColumnsViewed(e, clickedIndex, isSelected, previousValue);
    });

    var pred_centrewise_all_dist_timefilter = new google.visualization.ControlWrapper({'controlType':'DateRangeFilter', 'containerId':'pred_centrewise_all_dist_timefilter','options':{'filterColumnLabel':'Date','ui':{'label':'Choose a Time Frame'}}});
    pred_centrewise_all_dashboard.bind([pred_centrewise_all_dist_filter,pred_centrewise_all_dist_timefilter],pred_centrewise_all_dist_chart);
    pred_centrewise_all_dashboard.draw(pred_centrewise_all_dashboard_data);
    document.getElementById('prediction_content_div').style.display='none';"""
    
    
    
    
   
    str1+="""  }
    
            </script>"""
    #Ending of HTML Page
    str1+="""</body>
             </html>"""
    db.engine.execute("""DELETE FROM medicaldata;""")
    db.engine.execute("""DELETE FROM medicaldata_pred;""")
    db.engine.execute("""DELETE FROM outbreak_analysis;""")
    disdf=pd.read_sql("""SELECT Disease FROM diseases;""",db.engine)
    for i in disdf.values:
        db.engine.execute("""DELETE FROM """+i[0]+"""_Pred;""")
    
    #file store and add to db
    try:
        fd=open(dir,'w')
        fd.write(str1)
        fd.close()
        if(al==None):
            rep=reports(ReportTime=currtime,ReportLoc=filename)
        else:
            rep=reports(ReportTime=currtime,ReportLoc=filename,Algorithm=al)
        db.session.add(rep)
        db.session.commit()
    except FileExistsError as e:
        print("File Exists",e)
    print("Reports generated")
    