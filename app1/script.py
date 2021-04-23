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
from os import path
from pycaret.regression import *


pio.templates.default = "plotly_white"
#from ortools.sat.python import cp_model

def simple_fe(data):
    data['rate']=data['rate'].ffill()
    data['rate']=data['rate'].bfill()
    data['month']=data.index.month
    data['month'] = data['month'].astype('category')
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
    data['days'] = (data.index - pd.to_datetime('01012011', format='%d%m%Y')).days
    data['rolling_price_max_t6'] = data['rate'].transform(lambda x: x.shift(1).rolling(6).max())
    data['rolling_price_mean_t6'] = data['rate'].transform(lambda x: x.shift(1).rolling(6).mean())
    data['rolling_price_std_t6'] = data['rate'].transform(lambda x: x.rolling(6).std())
    data=data.replace([np.inf, -np.inf, np.nan], 0)
    '''
    dd=data[data['so_qty']>0]['so_qty']
    Q1 = dd.quantile(0.25)
    Q3 = dd.quantile(0.75)
    IQR = Q3 - Q1
    maxn= Q3 + 1.5 * IQR
    data['so_qty'].values[data['so_qty'] > maxn] = maxn'''
    #ts=4
    #trainx=data.drop(['so_qty'],axis=1)[:-ts]
    #testx=data.drop(['so_qty'],axis=1)[-ts:]
    #trainy=data['so_qty'][:-ts]
    #testy=data['so_qty'][-ts:]
    return data

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
        k='forecast/'+str(int(i))
        #if path.exists(k):
        #    pass
        #else:
        sl=df5[df5['code__id']==i]
        sl.drop('code__id',inplace=True,axis=1)
        data=simple_fe(sl)
        if len(data)>6:
            #trainx=trainx[['rate','month']]
            #try:
            numeric = ['lag_t1','lag_t2','lag_t3','lag_t4','lag_t5','lag_t6','lag_t12','rolling_mean_t6','rolling_mean_t12','rolling_max_t6',
            'rolling_max_t12','rolling_price_max_t6','rolling_price_mean_t6','rolling_price_std_t6','days']
            reg1 = setup(sl, target = 'so_qty',silent=True,train_size= 0.80,categorical_features = ['month'],numeric_features=numeric)
            print(sl.info())
            best_model = compare_models(fold=5)
            try:
                tuned_model = tune_model(best_model, n_iter=5, optimize = 'MAE')
                save_model(tuned_model, k)
            except:
                save_model(best_model, k)
            #save_model(tuned_model, model_name=k)
            #arima=auto_arima(y=trainy,seasonal=True,m=12,trace=True,stepwise=True)
            #except:
            #    pass
    
from pandas.tseries.offsets import MonthBegin
#from sqlalchemy.sql import text
from django.db.models import Case, Value, When
def genforecast(df5):
    #from sqlalchemy import create_engine
    #database_url = 'postgresql://admin:admin@localhost:5432/app1db'
    #engine = create_engine(database_url, echo=False)
    #print(df5.info())
    for i in df5['code__id'].unique():
        k='forecast/'+str(int(i))
        tdf=df5[df5['code__id']==i]
        if len(tdf)>1 and path.exists(k+'.pkl'):
            tdf['so_del']=tdf.index
            reg = load_model(k)
            #print(tdf)
            for c in range(12):
                tdf=tdf.tail(12)
                #print(tdf.tail(1)['so_del'].values[0])
                tmp={'code__id':tdf.tail(1)['code__id'].values[0],'rate':tdf.tail(1)['rate'].values[0],'so_del':pd.to_datetime(datetime.date.today()+ MonthBegin(n=c+1))}
                tdf=tdf.append(tmp,ignore_index=True)
                tdf.set_index('so_del',inplace=True)
                #print(tdf['so_qty'])
                data=simple_fe(tdf)
                data=data.drop(['so_qty'],axis=1)
                tt=predict_model(reg,data=data.tail(1))
                print(i,c,tt['Label'])
                ''' Working update
                if Forecast.objects.filter(code_id=i, month=pd.to_datetime(datetime.date.today()- MonthBegin(n=1)),version=c+1, dem_month=pd.to_datetime(datetime.date.today()+ MonthBegin(n=c+1))).exists():
                    Forecast.objects.update(fore_qty=Case(When(code_id=i, month=pd.to_datetime(datetime.date.today()- MonthBegin(n=1)),version=c+1, dem_month=pd.to_datetime(datetime.date.today()+ MonthBegin(n=c+1)), then=tt['Label'].values[0].item()),default=0))
                else:
                    Forecast.objects.create(code_id=i, month=pd.to_datetime(datetime.date.today()- MonthBegin(n=1)),version=c+1, dem_month=pd.to_datetime(datetime.date.today()+ MonthBegin(n=c+1)), fore_qty=tt['Label'].values[0].item())
            '''
            '''
            tdf['so_del']= pd.to_datetime(tdf['so_del'])
            tdf.set_index('so_del',inplace=True)
            #tdf['month']=tdf.index.month
            tdf['month'] = tdf['month'].astype('category')
            #print(k,path.exists(k))
            if path.exists(k+'.pkl'):
                reg = load_model(k)
                #print(tdf.info())
                tdf=tdf.drop(['code__id'],axis=1)
                data=simple_fe(tdf)
                data=data[data.index.date>datetime.date.today()]
                #print(data.info())
                data=data.drop(['so_qty'],axis=1)
                tt=predict_model(reg,data=data)
                print(tt)
                for c in range(12):
                    #query = text("""UPDATE app1_forecast SET fore_qty=:f WHERE code_id=:co AND month=:d AND dem_month=:g; 
                    #INSERT INTO app1_forecast(code_id,fore_qty,month,dem_month,version) SELECT :co,:f, :d,:g,:v WHERE NOT EXISTS (SELECT 1 FROM app1_forecast WHERE code_id=:co AND month=:d AND dem_month=:g)""")
                    #engine.execute(query, co=i,f=tt[c], d=pd.to_datetime(datetime.date.today()- MonthBegin(n=1)), g=pd.to_datetime(datetime.date.today()+ MonthBegin(n=c)),v=c+1)
                    Forecast.objects.update(fore_qty=Case(When(code_id=i, month=pd.to_datetime(datetime.date.today()- MonthBegin(n=1)), dem_month=pd.to_datetime(datetime.date.today()+ MonthBegin(n=c+1)), then=Value(tt.iloc[c,:]['Label']))))
'''
def savemodel(df5,pk):
    sl=simple_fe(df5)
    '''
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
        Fmodel.objects.filter(id=pk).update(model=model,smape=ss,mae=ma,mase=mas)'''
    reg1 = setup(sl, target = 'so_qty')
    best_model = compare_models(fold=5)

from pandas_profiling import ProfileReport
def exploremodel(df5,pk):
    sl=simple_fe(df5)
    #profile = ProfileReport(sl, title="Profiling Report",explorative=True, html={"navbar_show":False})
    #kk=profile.html
    reg1 = setup(sl, target = 'so_qty',silent=True,profile=True)
    #print(reg1)
    best_model = compare_models(fold=5)
    df=pull()
    tuned_model = tune_model(best_model, n_iter=50, optimize = 'MAE')
    ev= plot_model(tuned_model)
    ev1= plot_model(tuned_model,'feature_all')
    context = {'df': df.style.highlight_min().render(),'ev':ev,'ev1':ev1}
    return context

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
    explainer = shap.Explainer(reg.predict, trainx)
    shap_v= explainer(trainx)
    sk=px.box(pd.DataFrame(shap_v.values,columns=trainx.columns)).to_html(full_html=False)
    context = {'graph': graph, 'graph1':graph1,'smape':error,'mae':mae,'mase':mas,'code':row.code,'vis':sk}
    return context
    
def genmps(df5):
    qs= Forecast.objects.all()
    ff= ['code','dem_month','fore_qty','overr_qty','version','code_id','code__code']
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df['dem_month']=pd.to_datetime(df['dem_month'])
    df=df.sort_values(by=['code_id','version'])
    df=df.drop_duplicates(subset=['code_id', 'version'], keep='first')
    
    return df.to_html()
    '''
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
    explainer = shap.Explainer(reg.predict, trainx)
    shap_v= explainer(trainx)
    sk=px.box(pd.DataFrame(shap_v.values,columns=trainx.columns)).to_html(full_html=False)
    context = {'graph': graph, 'graph1':graph1,'smape':error,'mae':mae,'mase':mas,'code':row.code,'vis':sk}
    return context'''
    
