import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from models import reports
from datastore import db


def gen_report(launch_method='auto',algorithm=None):
    dir=os.getcwd()
    if(launch_method=='auto'):
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
        filename="""\\reports\\"""+currtime.strftime("%Y-%m-%d_00-00-00")+".html"
    else:
        currtime=datetime.strptime(datetime.now().strftime("%Y %m %d %H %M %S"),"%Y %m %d %H %M %S")
        filename="""\\reports\\"""+currtime.strftime("%Y-%m-%d_%H-%M-%S")+"_custom.html"
    dir=dir+filename
    print(dir)
    #data loading
    lastweek=currtime-timedelta(currtime.weekday())-timedelta(weeks=1,days=1)
    lastweek=datetime.strptime(lastweek.strftime("%Y %m %d 00 00 00"),"%Y %m %d %H %M %S")
    print("Lastweek:",lastweek)
    df=pd.read_sql("""SELECT Disease, sum(NoOfCases) as Count from medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Disease ORDER BY sum(NoOfCases) DESC""",db.engine)
    df2=pd.read_sql("""SELECT c.District, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, centreloc c WHERE m.CentreCode=c.CentreCode AND m.EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY c.District, m.Disease ORDER BY c.District, m.Disease""",db.engine)
    df3=pd.read_sql("""SELECT Age, count(Age)*NoOfCases as Count FROM medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY Age ORDER BY Age""",db.engine)
    df4=pd.read_sql("""SELECT sum(NoOfCases) as Count FROM medicaldata WHERE EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""'""",db.engine)
    last4wk=currtime-timedelta(currtime.weekday())-timedelta(weeks=4,days=1)
    last4wkstartdt=[]
    for i in range(0,4):
        last4wkstartdt.append(last4wk+timedelta(weeks=i))
    df5=pd.read_sql("""SELECT STRFTIME("%Y-%m-%d",EntryTime) as ETime, Disease, sum(NoOfCases) as Count FROM medicaldata WHERE  EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+last4wk.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY ETime,Disease ORDER BY ETime, Disease""",db.engine)
    df6=pd.read_sql("""SELECT STRFTIME("%Y-%m-%d",m.EntryTime) as ETime, c.District, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, centreloc c WHERE m.CentreCode=c.CentreCode AND m.EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND m.EntryTime>='"""+last4wk.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY ETime, c.District, m.Disease ORDER BY ETime, c.District, m.Disease""",db.engine)
    print(df6)
   
    lastwkstart=lastweek-timedelta(weeks=1)
    df7=pd.read_sql("""SELECT sum(NoOfCases) as Count FROM medicaldata WHERE EntryTime<='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastwkstart.strftime("%Y-%m-%d %H:%M:%S")+"""'""",db.engine)
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
    df8=pd.read_sql("""SELECT c.District, sum(m.NoOfCases) as Count FROM centreloc c, medicaldata m WHERE m.CentreCode=c.CentreCode AND m.EntryTime<='"""+currtime.strftime("%Y-%m-%d %H:%M:%S")+"""' AND EntryTime>='"""+lastweek.strftime("%Y-%m-%d %H:%M:%S")+"""' GROUP BY m.CentreCode ORDER BY Count DESC""",db.engine)
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
                <h5>Report Generated at: """+currtime.strftime("%d-%m-%Y %H:%M")+"""</h5>
                <div style='margin-left:15px; margin-right:15px; margin-bottom:10px; border:2px solid #CFCFCF; padding:4px; border-radius:6px;'>
                        <h3>Predictions:</h3>
                        <div class='row' style='margin:5px; margin-left:15px;'>
                        <div class='col-lg-6'>
                        1. Number of new cases this week: """+str(df4.values[0][0])+""" cases <br/>
                        2. Change in cases from last week: """+changeinwk+"""% ("""+changeinwk2+""" cases)<br/>
                        3. Most infectious disease: """+df.values[0][0]+""" <br/>
                        4. Most infected age group: """+maxagerange+"""<br/>
                        5. Disease showing most improvement from last week: """+str(0)+"""<br/>
                        6. Region with highest cases this week: """+df8.values[0][0]+""" <br/>
                        7. Region with least cases this week: """+df8.values[-1][0]+"""<br/>
                        8. Statistic: """+str(0)+"""<br/>                        
                        </div>
                        <div class='col-lg-6'>"""
    if(algorithm!=None):
        str1+="""9.&nbsp; Prediction Algorithm Used: """+algorithm+""" <br/>"""
    else:
        str1+="""9.&nbsp;&nbsp;Statistic: """+str(0)+"""<br/>
                        10. Statistic: """+str(0)+""" <br/>
                        11. Statistic: """+str(0)+""" <br/>
                        12. Statistic: """+str(0)+"""<br/>
                        13. Statistic: """+str(0)+""" <br/>
                        14. Statistic: """+str(0)+"""<br/>
                        15. Statistic: """+str(0)+"""<br/>
                        16. Statistic: """+str(0)+"""<br/>
                        </div>
                        </div>
                </div>
                <div id='pred_age_distribution_table'></div>
                <div id='pred_age_distribution_chart'></div>
                <div id='pred_disease_distribution_table'></div>
                <div id='pred_disease_distribution_chart'></div>
                <div id='pred_centrewise_top10_dist_table'></div>
                <div id='pred_centrewise_top10_dist_chart' style='height:100%'></div>
                <div id='pred_4week_trendline'></div>
                
            </div>
            
            <div id='report_content_div' style='width:100%;margin-top:5px;'>
                <h5 style='margin-left:5px;'>Report Generated at: """+currtime.strftime("%d-%m-%Y %H:%M")+"""</h5>
                <div style='margin-left:15px; margin-right:15px; margin-bottom:10px; border:2px solid #CFCFCF; padding:4px; border-radius:6px;'>
                        <h3>Useful Stats:</h3>
                        <div class='row' style='margin:5px; margin-left:15px;'>
                        <div class='col-lg-6'>
                        1. Number of new cases this week: """+str(df4.values[0][0])+""" cases <br/>
                        2. Change in cases from last week: """+changeinwk+"""% ("""+changeinwk2+""" cases)<br/>
                        3. Most infectious disease: """+df.values[0][0]+""" <br/>
                        4. Most infected age group: """+maxagerange+"""<br/>
                        5. Disease showing most improvement from last week: """+str(0)+"""<br/>
                        6. Region with highest cases this week: """+df8.values[0][0]+""" <br/>
                        7. Region with least cases this week: """+df8.values[-1][0]+"""<br/>
                        8. Statistic: """+str(0)+"""<br/>                        
                        </div>
                        <div class='col-lg-6'>
                        9.&nbsp; Statistic: """+str(0)+""" <br/>
                        10. Statistic: """+str(0)+""" <br/>
                        11. Statistic: """+str(0)+""" <br/>
                        12. Statistic: """+str(0)+"""<br/>
                        13. Statistic: """+str(0)+""" <br/>
                        14. Statistic: """+str(0)+"""<br/>
                        15. Statistic: """+str(0)+"""<br/>
                        16. Statistic: """+str(0)+"""<br/>
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

                    
                    var pred_age_distribution_chart = new google.visualization.PieChart(document.getElementById('pred_age_distribution_chart'));
                    var pred_age_distribution_table = new google.visualization.Table(document.getElementById('pred_age_distribution_table'));
                    var pred_disease_distribution_table = new google.visualization.Table(document.getElementById('pred_disease_distribution_table'));
                    var pred_disease_distribution_chart = new google.visualization.PieChart(document.getElementById('pred_disease_distribution_chart'));  var pred_centrewise_top10_dist_table = new google.visualization.Table(document.getElementById('pred_centrewise_top10_dist_table'));
                    var pred_centrewise_top10_dist_chart = new google.charts.Bar(document.getElementById('pred_centrewise_top10_dist_chart'));
                    var pred_x4week_trendline = new google.visualization.LineChart(document.getElementById('pred_4week_trendline'));
                    
                
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
    print(df2)
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
    print(df5)
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
    for i in range(0,56):
        last8wkdt.append(last8wk+timedelta(days=i))
    print(last8wkdt)
    dfmain=pd.DataFrame()
    print(dfmain)
    for i in range(len(last8wkdt)):
        df6=pd.read_sql("""SELECT c.District, STRFTIME("%Y-%m-%d",m.EntryTime) as ETime, m.Disease, sum(m.NoOfCases) as Count FROM medicaldata m, centreloc c WHERE m.CentreCode=c.CentreCode AND ETime='"""+last8wkdt[i].strftime("%Y-%m-%d")+"""' GROUP BY c.District, m.Disease ORDER BY c.District, m.Disease""",db.engine)
        df6=df6.drop('ETime',axis=1)
        df6=df6.pivot(index='District',columns='Disease')
        df6=df6.fillna(0)
        dates=[]
        for j in range(df6.shape[0]):
            dates.append(last8wkdt[i].strftime("%Y-%m-%d"))
        df6.insert(loc=len(df6.columns),column='ETime',value=dates)
        dfmain=pd.concat([dfmain,df6])
        dfmain=dfmain.fillna(0)    
        print(dfmain.values)
    str1+="""   var centrewise_all_dashboard_data = new google.visualization.DataTable();
                centrewise_all_dashboard_data.addColumn('date','Date');
                centrewise_all_dashboard_data.addColumn('string','District');"""
    for i in range(0,len(dfmain.columns)-1):
        str1+="""centrewise_all_dashboard_data.addColumn('number','"""+dfmain.columns[i][1]+"""');"""
    for i in range(len(dfmain.values)):
        str1+="""centrewise_all_dashboard_data.addRow([new Date('"""+str(dfmain.values[i][-1])+"""T00:00:00+05:30'),'"""+str(dfmain.index[i])+"""'"""
        for j in range(0,len(dfmain.values[i])-1):
            print(dfmain.values[i][j])
            str1+=""","""+str(round(dfmain.values[i][j],0))
        str1+="""]);"""

    str1+="""var centrewise_all_dist_chart = new google.visualization.ChartWrapper({'chartType':'LineChart','containerId':'centrewise_all_dist_chart','options':{'title':'Disease Trends By Region (max. past 8 weeks)','fontSize':'10','titleTextStyle':{'color':'black','fontName':'Arial','fontSize':'16','bold':'true','italic':'false'},'hAxis':{'title':'No. of Cases'},'vAxis':{'title':'New Cases per Day'},'width':'100%','height':'400px'},'view':{'columns':[0"""
    for i in range(len(dfmain.columns)-1):
        str1+=""","""+str(i+2)
    str1+="""]}});
    var centrewise_all_dist_filter = new google.visualization.ControlWrapper({'controlType':'CategoryFilter', 'containerId':'centrewise_all_dist_filter','options':{'filterColumnLabel':'District','ui':{'allowTyping':false,'allowMultiple':false,'allowNone':false,'label':'Choose a Region'}}});


    function changeColumnsViewed(e, clickedIndex, isSelected, previousValue){
        console.log($('.selectpicker').selectpicker('val'));
        console.log(centrewise_all_dashboard_data);
        console.log(centrewise_all_dist_chart.getView());
        selectedValues=$('.selectpicker').selectpicker('val');
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
    for i in range(0,len(dfmain.columns)):
        str1+="""<option>"""+dfmain.columns[i][1]+"""</option>"""
    str1+="""';
    $('.selectpicker').selectpicker('refresh');
    $('.selectpicker').on('changed.bs.select', function (e, clickedIndex, isSelected, previousValue) {
            changeColumnsViewed(e, clickedIndex, isSelected, previousValue);
    });

    var centrewise_all_dist_timefilter = new google.visualization.ControlWrapper({'controlType':'DateRangeFilter', 'containerId':'centrewise_all_dist_timefilter','options':{'filterColumnLabel':'Date','ui':{'label':'Choose a Time Frame'}}});
    centrewise_all_dashboard.bind([centrewise_all_dist_filter,centrewise_all_dist_timefilter],centrewise_all_dist_chart);
    centrewise_all_dashboard.draw(centrewise_all_dashboard_data);"""
    print(str1)
    str1+="""  }
    
            </script>"""
    #Ending of HTML Page
    str1+="""</body>
             </html>"""

    #file store and add to db
    try:
        fd=open(dir,'w')
        fd.write(str1)
        fd.close()
        if(algorithm==None):
            rep=reports(ReportTime=currtime,ReportLoc=filename)
        else:
            rep=reports(ReportTime=currtime,ReportLoc=filename,Algorithm=algorithm)
        db.session.add(rep)
        db.session.commit()
    except FileExistsError as e:
        print("File Exists",e)
    print("Reports generated")
    
    #Add prediction table deletion code
    