import panel as pn
import pandas as pd
import altair as alt
import numpy as np
import lightgbm as lgb
import xgboost as xgb


pn.extension(design='bootstrap')
pn.extension('vega', template='bootstrap')
alt.data_transformers.disable_max_rows()
alt.renderers.enable('default')
@pn.cache()
def ld():
    df=pd.read_excel("/home/swastik/Downloads/MTPastData11052023.xlsx",sheet_name='POS Data 2019-2023')
    #df2=pl.from_pandas(df)
    df=df.drop(columns=['Q1','Q2','Q3','Q4','Total','Seq 5 Descripton','Final\n Classification','Status','Customer'])
    df=df.melt(['SKU Code','Description','Year'])
    df=df.rename(columns={'variable':'month','value':'sale'})
    #df2=df2.with_columns((df2['month']+'-'+df2['Year']).alias('date'))
    df['date']=df['month']+'-'+df['Year'].astype('str')
    #df2=df2.with_columns(pl.col('date').str.strptime(pl.Date,format='%b-%Y'))
    df['date']=pd.to_datetime(df['date'],format=f"%b-%Y")
    df['Year'] = df['Year'].astype('category')
    return df
df=ld()
ss=pn.widgets.MultiChoice(name='SKU',options=list(df['SKU Code'].unique()),max_items=1,value=['CEL1000041'])

def fe(df):
    data=df.copy()
    #data['date']<pd.Timestamp.today()-pd.offsets.MonthBegin(normalize=True)
    data['month']=data['date'].dt.month
    data['month'] = data['month'].astype('category')
    data['lag_t6'] = data['sale'].transform(lambda x: x.shift(6))
    #data['lag_t5'] = data['sale'].transform(lambda x: x.shift(5))
    #data['lag_t4'] = data['sale'].transform(lambda x: x.shift(4))
    data['lag_t3'] = data['sale'].transform(lambda x: x.shift(3))
    data['lag_t2'] = data['sale'].transform(lambda x: x.shift(2))
    data['lag_t1'] = data['sale'].transform(lambda x: x.shift(1))
    data['lag_t12'] = data['sale'].transform(lambda x: x.shift(12))
    data['rolling_mean_t6'] = data['sale'].transform(lambda x: x.rolling(6).mean())
    data['rolling_mean_t3'] = data['sale'].transform(lambda x: x.rolling(3).mean())
    data['rolling_std_t6'] = data['sale'].transform(lambda x: x.rolling(6).std())
    #data['rolling_mean_t12'] = data['sale'].transform(lambda x: x.rolling(12).mean())
    data['rolling_max_t6'] = data['sale'].transform(lambda x: x.rolling(6).max())
    #data['rolling_max_t12'] = data['sale'].transform(lambda x: x.rolling(12).max())
    data['days'] = (data['date'] - pd.to_datetime(min(data['date']))).dt.days
    data=data.replace(np.inf,2*max(data['sale']) )
    data=data.replace(-np.inf,2*max(data['sale']) )
    data=data.bfill()
    data=data.drop(columns=['date','SKU Code','Year'])
    #data['rolling_mean_t12'] = data['rolling_mean_t12'].fillna(data['rolling_mean_t6'])
    #data['rolling_max_t12'] = data['rolling_mean_t12'].fillna(data['rolling_max_t6'])
    return data


def model(ss,df):
    df2=df[df['SKU Code'].isin(ss)]
    df2=df2[df2['date']<(pd.Timestamp.today()-pd.offsets.MonthBegin(3,normalize=True))]
    df2=df2.groupby(['SKU Code','date']).sum(numeric_only=True).reset_index()
    df2=df2.sort_values(['SKU Code','date'])
    print(df2)
    df2=df2.drop(columns=['date','SKU Code'])
    #ff=fe(df2)
    param = {'num_leaves': 31, 'objective': 'binary'}
    param['metric'] = 'auc'
    #ld= lgb.Dataset(df2,label='sale')
    #bst= lgb.cv(param, ld, 10)
    #pr=bst.predict()
    df2=df2.reset_index(drop=True)
    
    xtr=df2.drop(columns='sale').iloc[:int(np.round(.95*len(df2))),:]
    xte=df2.drop(columns='sale').iloc[int(np.round(.95*len(df2))):,:]
    ytr=df2['sale'].iloc[:int(np.round(.95*len(df2)))]
    yte=df2['sale'].iloc[int(np.round(.95*len(df2))):]
    gbm = lgb.LGBMRegressor(num_leaves=31,learning_rate=0.05,n_estimators=20)
    gbm.fit(xtr,ytr)
    pr=gbm.predict(xte)
    return pr

@pn.depends(ss)
def chart(ss):
    if ss:
        df1=df[df['SKU Code'].isin(ss)]
    else:
        df1=df.copy()
    sk=alt.selection_point(fields=['SKU Code'])
    fig3=alt.Chart(df1).encode(y=alt.Y('[SKU Code]:N',sort=alt.EncodingSortField(field='sum_sale', order='descending',op='sum')),x='sum(sum_sale):Q',tooltip=['[SKU Code]:N','sum(sum_sale):Q','Description:N'],color=alt.condition(sk,alt.value('blue'), alt.value('lightgray')))\
        .mark_bar(opacity=0.4,order=True).properties(width=400).add_params(sk).transform_aggregate(sum_sale='sum(sale):Q',groupby=['SKU Code','Description']
).transform_window(window=[{'op': 'rank', 'as': 'rank'}],sort=[{'field': 'sum_sale', 'order': 'descending'}]).transform_filter('datum.rank <= 40')
    base=alt.Chart(df1).encode(x='date:T',y='sum(sale):Q').transform_filter(sk)
    fig=base.mark_line(opacity=0.7).properties(height=210,width=800)
    fig1=base.mark_point(size=85,opacity=0.02).encode(tooltip=['date:T','sum(sale):Q']).interactive().properties(height=210,width=800)
    fig2=alt.Chart(df1).encode(x='month(date):T',y='sum(sale):Q',color='Year:N',xOffset="Year:N",tooltip=['date:T','sum(sale):Q'])\
        .mark_bar(opacity=0.85).properties(height=260,width=800).transform_filter(sk)
    pr=model(ss,df1)
    print(pr)
    return (fig3|(fig2&(fig+fig1))).configure_axis(grid=False)


pn.Column(ss,chart).servable()
#pn.Column(model()).servable()
