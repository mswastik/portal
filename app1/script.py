import pandas as pd
import numpy as np
from django_pandas.io import read_frame
import plotly.express as px
import plotly.tools as tls
from statsmodels.tools.eval_measures import rmse
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.inspection import permutation_importance
import datetime
from dateutil import relativedelta
import joblib
from .models import Forecast
from pandas.tseries.offsets import DateOffset

import collections
from ortools.sat.python import cp_model

def genmodel(df):
    df1=df.set_index('so_del_date')
    df1=df1.groupby(['code__id','rate']).resample('M').sum()[['so_qty']]
    df1=df1.reset_index()
    df1['year']=df1.so_del_date.dt.year
    df1['month']=df1.so_del_date.dt.month
    df1['days'] = (df1['so_del_date'] - df1['so_del_date'].min()).dt.days
    reg={}
    for i in df1['code__id'].unique():
        sl=df1[df1['code__id']==i]
        trainx = sl[['rate','year','month','days']].to_numpy()
        trainy= sl['so_qty'].to_numpy()
        reg[i] = RandomForestRegressor(random_state=0,max_depth=6)
        reg[i].fit(X=trainx,y=trainy)
    joblib.dump(reg, 'app1/forecast.joblib')  
    
def genforecast(df):
    reg = joblib.load('app1/forecast.joblib')
    tdf=pd.DataFrame()
    df5 = pd.DataFrame()
    for i in df['code__id'].unique():
        tt={}
        if len(df[df['code__id']==i])>3:
            rate= df[df['code__id']==i].sort_values('days',ascending=False)['rate'].head(1).values[0]
            for m in range(0,3):
                month = (datetime.date.today()+relativedelta.relativedelta(months=+m+1)).month
                year = (datetime.date.today()+relativedelta.relativedelta(months=+m+1)).year
                days = (datetime.date.today()+relativedelta.relativedelta(months=+m+1)-df['so_del_date'].min().date()).days
                tdf=tdf.append({'code__id':i,'rate':rate,'year':year,'month':month,'days':days},ignore_index=True)

    for i in tdf['code__id'].unique():
        slt=tdf[tdf['code__id']==i]
        slt.pop('code__id')
        if len(slt)>0:
            df5=df5.append({'code_id':i,'pred':reg[i].predict(X=slt[['rate','year','month','days']].to_numpy())},ignore_index=True)
    k=df5['pred'].apply(pd.Series)
    k.columns = [1,2,3]
    df5=pd.concat([df5,k],axis=1)
    df5.pop('pred')
    df5=df5.melt('code_id')
    df5['code_id']=df5['code_id'].astype('int')
    df5['month']=pd.to_datetime(datetime.date.today())
    df5.rename(columns={'variable':'version','value':'fore_qty'},inplace=True)
    df5['dem_month'] = df5['version'].apply(lambda x: DateOffset(months=x)+pd.datetime.today())
    from sqlalchemy import create_engine
    #import psycopg2
    database_url = 'postgresql://admin:admin@localhost:5432/app1db'
    engine = create_engine(database_url, echo=False)
    #conn = psycopg2.connect("dbname=app1db user=admin password=admin")
    df5.to_sql('app1_forecast', con=engine,if_exists='append',index=False)
