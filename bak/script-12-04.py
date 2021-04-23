import pandas as pd
import numpy as np
from django_pandas.io import read_frame
import plotly.express as px
import plotly.tools as tls
import plotly.graph_objects as go
from statsmodels.tools.eval_measures import rmse
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split,cross_val_score
from sklearn.inspection import permutation_importance
import datetime
from dateutil import relativedelta
import joblib
import pickle
from sklearn.model_selection import GridSearchCV
from .models import Forecast,Fmodel
from pandas.tseries.offsets import DateOffset
import collections
import plotly.io as pio
from sklearn.metrics import make_scorer,mean_absolute_error
from sklearn import svm
from pmdarima.arima import auto_arima
from sklearn.linear_model import Lasso
from pmdarima.model_selection import cross_val_score as cvs
import pmdarima as pmd

pio.templates.default = "plotly_white"
#from ortools.sat.python import cp_model

def simple_fe(data):
    data['rate']=data['rate'].ffill()
    data['lag_t6'] = data['so_qty'].transform(lambda x: x.shift(6))
    data['lag_t5'] = data['so_qty'].transform(lambda x: x.shift(5))
    data['lag_t4'] = data['so_qty'].transform(lambda x: x.shift(4))
    data['lag_t3'] = data['so_qty'].transform(lambda x: x.shift(3))
    data['lag_t2'] = data['so_qty'].transform(lambda x: x.shift(2))
    data['lag_t1'] = data['so_qty'].transform(lambda x: x.shift(1))
    data['lag_t12'] = data['so_qty'].transform(lambda x: x.shift(12))
    data['rolling_mean_t6'] = data['so_qty'].transform(lambda x: x.rolling(6).mean())
    data['rolling_std_t6'] = data['so_qty'].transform(lambda x: x.rolling(6).std())
    data['rolling_mean_t12'] = data['so_qty'].transform(lambda x: x.rolling(12).mean())
    data['rolling_max_t6'] = data['so_qty'].transform(lambda x: x.rolling(6).max())
    data['rolling_max_t12'] = data['so_qty'].transform(lambda x: x.rolling(12).max())
    data['days'] = (data.index - data.index.min()).days
    data['rolling_price_max_t6'] = data['rate'].transform(lambda x: x.shift(1).rolling(6).max())
    data['rolling_price_mean_t6'] = data['rate'].transform(lambda x: x.shift(1).rolling(6).mean())
    data['rolling_price_std_t6'] = data['rate'].transform(lambda x: x.rolling(6).std())
    data=data.replace([np.inf, -np.inf, np.nan], 0)
    dd=data[data['so_qty']>0]['so_qty']
    Q1 = dd.quantile(0.25)
    Q3 = dd.quantile(0.75)
    IQR = Q3 - Q1
    maxn= Q3 + 1.5 * IQR
    data['so_qty'].values[data['so_qty'] > maxn] = maxn
    ts=4
    trainx=data.drop(['so_qty'],axis=1)[:-ts]
    testx=data.drop(['so_qty'],axis=1)[-ts:]
    trainy=data['so_qty'][:-ts]
    testy=data['so_qty'][-ts:]
    return trainx,testx,trainy,testy

def smape(A, F):
    return round(100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F))),2)

def mase(A, F):
    errors = np.mean(np.abs(A - F))
    try:
        return round(errors / np.mean(np.abs(A-A.mean())),2)
    except:
        return 0 

def genmodel(df5):
    reg={}
    for i in df5['code__id'].unique():
        sl=df5[df5['code__id']==i]
        trainx,testx,trainy,testy=simple_fe(df5)
        la_grid = {'alpha': [.1,.3,.4,.5,.6,.8]}
        la = Lasso()
        gs = GridSearchCV(la, la_grid, cv=5)
        gs.fit(X=trainx,y=trainy)
        reg[i] = gd.best_estimator_
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
   

def savemodel(df5,pk):
    trainx,testx,trainy,testy=simple_fe(df5)
    obj=Fmodel.objects.get(id=pk).alg
    #al = getattr(obj, field_name)
    if obj=='ARIMAX':
        #print(trainx.info())
        trainx=trainx[['rate','month']]
        arima=auto_arima(y=trainy,X=trainx,seasonal=True,m=12,trace=True,stepwise=True)
        model=pickle.dumps(arima)
        cv = pmd.model_selection.SlidingWindowForecastCV(step=1, h=4)
        ss=cvs(arima,trainy,trainx,cv=cv,scoring='smape').mean()
        ma=cvs(arima,trainy,trainx,cv=cv,scoring='mean_absolute_error').mean()
        mas=cvs(arima,trainy,trainx,cv=cv,scoring=mase).mean()
        if np.isinf(mas):
            mas=0
        Fmodel.objects.filter(id=pk).update(model=model,smape=ss,mae=ma,mase=mas)
    else:    
        if obj=='Random Forrest':
            rf_grid = {'max_depth': [5,10,15],'min_samples_split': [2,3, 5, 8]}
            rf = RandomForestRegressor()
            gs = GridSearchCV(rf, rf_grid, cv=5)
            gs.fit(X=trainx,y=trainy)
        elif obj=='SVM':
            sv_grid = {'kernel': ['poly', 'rbf', 'sigmoid',],'epsilon': [.1,.2,.3, .4],'C':[1,2,3,4]}
            sv = svm.SVR()
            gs = GridSearchCV(sv, sv_grid, cv=5)
            gs.fit(X=trainx,y=trainy)
        elif obj=="Linear Regression":
            la_grid = {'alpha': [.1,.3,.4,.5,.6,.8]}
            la = Lasso()
            gs = GridSearchCV(la, la_grid, cv=5)
            gs.fit(X=trainx,y=trainy)
        model=pickle.dumps(gs.best_estimator_)
        ss=cross_val_score(gs.best_estimator_,trainx,trainy,cv=5,scoring=make_scorer(smape, greater_is_better=False)).mean()
        ma=cross_val_score(gs.best_estimator_,trainx,trainy,cv=5,scoring='neg_mean_absolute_error').mean()
        mas=cross_val_score(gs.best_estimator_,trainx,trainy,cv=5,scoring=make_scorer(mase, greater_is_better=False)).mean()
        Fmodel.objects.filter(id=pk).update(model=model,smape=ss,mae=ma,mase=mas)

from yellowbrick.regressor import PredictionError, ResidualsPlot
import shap
import matplotlib.pyplot as plt, mpld3
def genforecast1(df5,pk):
    kk = px.box(df5['so_qty'],width=400)
    fig1 = go.Figure(data=kk)
    graph1=fig1.to_html(full_html=False,config={'editable':False})
    row = Fmodel.objects.get(id=pk)
    reg = pickle.loads(row.model)
    trainx,testx,trainy,testy=simple_fe(df5)
    obj=Fmodel.objects.get(id=pk).alg
    if obj=='ARIMAX':
        testx=testx[['rate','month']]
        y_pred=reg.predict(4,X=testx)
    else:
        y_pred=reg.predict(X=testx)
    fig = go.Figure(layout={'width':800})
    #fig.add_scatter(x=trainx.index, y=trainy)
    fig.add_trace(go.Scatter(x=trainx.index, y=trainy, mode="lines+markers"))
    fig.add_trace(go.Scatter(x=testy.index, y=testy, mode="lines+markers",name='actual'))
    fig.add_trace(go.Scatter(x=testy.index, y=y_pred, mode="lines+markers",name='pred'))
    graph = fig.to_html(full_html=False,config={'editable':False})
    error=smape(testy,y_pred)
    mae=round(mean_absolute_error(testy,y_pred),2)
    mas=mase(testy,y_pred)
    #visualizer = ResidualsPlot(reg).fit(trainx,trainy)
    explainer = shap.Explainer(reg.predict, trainx)
    shap_v= explainer(trainx)
    #ss=shap.plots.bar(shap_v)
    #print(pd.DataFrame(shap_v.values,columns=trainx.columns))
    #sk=''
    sk=px.box(pd.DataFrame(shap_v.values,columns=trainx.columns)).to_html(full_html=False)
    context = {'graph': graph, 'graph1':graph1,'smape':error,'mae':mae,'mase':mas,'code':row.code,'vis':sk}
    return context
    
