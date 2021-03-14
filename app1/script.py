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

def genmodel(df5):
    reg={}
    for i in df5['code__id'].unique():
        sl=df5[df5['code__id']==i]
        sl=pd.get_dummies(sl,drop_first=True)
        sl=sl[sl['train_train']==1]
        trainx = sl.drop(['code__id','so_del_date','so_qty','train_train'],axis=1).to_numpy()
        trainy= sl['so_qty'].to_numpy()
        reg[i] = RandomForestRegressor(random_state=0,max_depth=6)
        reg[i].fit(X=trainx,y=trainy)
    joblib.dump(reg, 'app1/forecast.joblib')  
    
def genforecast(df5):
    reg = joblib.load('app1/forecast.joblib')
    tdf=pd.DataFrame()
    df6=pd.DataFrame()
    for i in df5['code__id'].unique():
        slt=df5[df5['code__id']==i]
        slt=pd.get_dummies(slt,drop_first=True)
        slt=slt[slt['train_train']==0]
        #slt=slt.drop(['code_id','so_del_date','so_qty','train_train'],axis=1)
        #df6['predictions'] = df[['input1','input2']].apply(lambda x: model.predict([x])[0],axis=1)
        df6=df6.append({'code_id':i,'pred':reg[i].predict(X=slt.drop(['code__id','so_del_date','so_qty','train_train'],axis=1).to_numpy())},ignore_index=True)
        
    k=df6['pred'].apply(pd.Series)
    k.columns = [1,2,3,4]
    df6=pd.concat([df6,k],axis=1)
    df6.pop('pred')
    df6=df6.melt('code_id')
    df6['code_id']=df6['code_id'].astype('int')
    df6['month']=pd.to_datetime(datetime.date.today())
    df6.rename(columns={'variable':'version','value':'fore_qty'},inplace=True)
    df6['dem_month'] = df6['version'].apply(lambda x: DateOffset(months=x)+pd.datetime.today())
    from sqlalchemy import create_engine
    #import psycopg2
    database_url = 'postgresql://admin:admin@localhost:5432/app1db'
    engine = create_engine(database_url, echo=False)
    #conn = psycopg2.connect("dbname=app1db user=admin password=admin")
    df6.to_sql('app1_forecast', con=engine,if_exists='append',index=False)
