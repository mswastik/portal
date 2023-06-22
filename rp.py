from sanic import Sanic
from reactpy import component, html, run, use_callback,use_state,web,utils
from reactpy.backend.sanic import configure,Options
from turbodbc import connect, make_options, Megabytes
import json
import io
import pandas as pd
import altair as alt
import uvicorn
import vegafusion as vf

#vf.enable_widget()

#alt.renderers.enable('svg')
alt.data_transformers.disable_max_rows()
headv=html._(html.link({"rel":"stylesheet","href":"https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.5.0/semantic.min.css"}),
                html.script({'src':"https://code.jquery.com/jquery-3.1.1.min.js",'integrity':"sha256-hVVnYaiADRTO2PzUGmuLJr8BLUSjGIZsDYGmIJLv2b8=",'crossorigin':"anonymous"}),
                html.script({"src":"https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.5.0/semantic.min.js","integrity":"sha512-Xo0Jh8MsOn72LGV8kU5LsclG7SUzJsWGhXbWcYs2MAmChkQzwiW/yTQwdJ8w6UA9C6EVG18GHb/TrYpYCjyAQw==","crossorigin":"anonymous", "referrerpolicy":"no-referrer"}),
                html.script({"src":"https://cdn.jsdelivr.net/npm/vega@5"}),
                html.script({"src":"https://cdn.jsdelivr.net/npm/vega-lite@5"}),
                html.script({"src":"https://cdn.jsdelivr.net/npm/vega-embed@6"}),
                )

options = make_options(read_buffer_size=Megabytes(300),
                        parameter_sets_to_buffer=1000,
                        varchar_max_character_limit=1000,
                        use_async_io=True,
                        prefer_unicode=True,
                        large_decimals_as_64_bit_types=True,
                        limit_varchar_results_to_max=True)

def alt_theme():
    return {
        'config': {
            'view':{
                'stroke':'transparent'
            },
            'title': {
                'titleColor':'#616161',
                'color':'#424242'
            },
            'axis': {
                'gridColor':'#EEEEEE',
                'titleFontSize':14,
                'labelFontSize':13,
                'titleFontStyle':500
            },
            "range": {
                "category": ["#6002ee", "#41c300", "#d602ee", "#ee6002", "#09ab3b"],
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
             } }
    }
alt.themes.register("alt_theme", alt_theme)
alt.themes.enable("alt_theme")

fran=['CMF','Instruments','Joint Replacement', 'Trauma and Extremities','Endoscopy','Spine']
coun=['INDIA', 'CHINA','UNITED STATES','JAPAN']

def data(co,fr,uni,pwi):
    ss="estus2sqlenvisionprd01.database.windows.net"
    cnxn=connect(DRIVER='ODBC Driver 17 for SQL Server',server=ss,user=f'{uni}@estus2sqlenvisionprd01',password=pwi,database="Envision",Trusted_Connection='yes', turbodbc_options=options)
    query = '''SELECT [Country],p.Franchise,p.[IBP Level 5],p.[CatalogNumber],SUM([EBS_SH_REQ_QTY_RD]) AS [`Act Orders Rev],sum(XX_FINAL_DPFCST) as [`Fcst DF Final Rev],sum(XX_MODREV_OVRD) as [`Fcst Stat Final Rev],[SALES_DATE] AS [firstofmonth],
        sum(s."`L2 DF Final Rev") AS [L2 DF Final Rev],sum(s.xx_l3_fstat_rev) as [L2 Stat Final Rev] 
        FROM [DWH].[Fact_Sales] s 
        JOIN [dwh].[dim_demantraproducts] p ON s.item_skey = p.item_skey 
        JOIN [dwh].[Dim_DemantraLocation] l ON s.Location_sKey = l.Location_skey 
        WHERE ([SALES_DATE] BETWEEN DATEADD(month, -24, GETDATE()) AND DATEADD(month, 12, GETDATE())) AND p.Franchise IN (?,?,?,?,?,?) AND l.[Country]=? 
        GROUP BY [Country],p.Franchise,p.[IBP Level 5],p.[CatalogNumber],[SALES_DATE]'''
    cur=cnxn.cursor()
    print('PULLING DATA!!')
    print([fr[i] for i in range(len(fr)) if fr[i]]+ ['' for i in range(len(fran)-len(fr))] + [co])
    cur.execute(query,[fr[i] for i in range(len(fr)) if fr[i]]+ ['' for i in range(len(fran)-len(fr))] + [co])
    dd=cur.fetchallnumpy()
    print('DONE!!')
    df=pd.DataFrame(dd)
    cnxn.close()
    cur.close()
    return df



@component
def tchart(df,l2fc,l0fc,fci,ski,cc):
    def cont(df,l2fc,l0fc,fci):
        if not df.empty:
            acc=df.copy()
            acc['L2 Abs Var']=abs(acc['`Act Orders Rev']-acc[l2fc])
            acc['L2 Acc']=1-acc['L2 Abs Var']/acc['`Act Orders Rev']
            acc.loc[acc['`Act Orders Rev']==0,'L2 Acc']=1
            acc['L2 Acc']=acc['L2 Acc'].clip(0,None)
            acc1=acc[(acc['firstofmonth']>=pd.Timestamp.today()-pd.offsets.MonthBegin(4,normalize=True)) & (acc['firstofmonth']<=pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True))]
            acc1['orders cont']=acc1['`Act Orders Rev']/acc1['`Act Orders Rev'].sum()*100
            acc1['var cont']=acc1['L2 Abs Var']/acc1['L2 Abs Var'].sum()*100
            acc1=acc1[['CatalogNumber','firstofmonth','orders cont','var cont']]
            acc=acc.merge(acc1,on=['CatalogNumber','firstofmonth'],how='left')
            acc.sort_values('`Act Orders Rev',ascending=False)
            its=alt.selection_point(fields=['CatalogNumber'])
            #highlight = alt.selection_point(on='mouseover',fields=['firstofmonth'], nearest=True, empty=True)
            c1=alt.Chart(acc[acc['firstofmonth']==pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True)]).mark_circle(color='#26A69A').encode(
                x=alt.X('sum(orders cont):Q',scale=alt.Scale(type="pow",exponent=0.3)),y=alt.Y('sum(var cont):Q',scale=alt.Scale(type="pow",exponent=0.3)),size=alt.Size('sum(`Act Orders Rev):Q', scale=alt.Scale(range=[100,700])),tooltip=['CatalogNumber:O','IBP Level 5:O']
                ,opacity=alt.condition(its, alt.value(.75), alt.value(0.08))).properties(height=400,width=700).add_params(its)
            c2=alt.Chart(acc).mark_line(color="#F57F17").encode(x='firstofmonth:T',y=alt.Y("`Act Orders Rev",'sum',title=''),tooltip=['firstofmonth','sum(`Act Orders Rev):Q']).properties(height=390,width=500).transform_filter(its)
            c3=alt.Chart(acc).mark_line(color='#42A5F5').encode(x='firstofmonth:T',y=alt.Y(l2fc,'sum',title='L2 '+fci),tooltip=['firstofmonth',f'sum({l2fc}):Q']).transform_filter(its)
            c4=alt.Chart(acc).mark_line(color='#E91E63').encode(x='firstofmonth:T',y=alt.Y(l0fc,'sum',title='Fcst '+fci),tooltip=['firstofmonth',f'sum({l0fc}):Q']).transform_filter(its)
            c41=alt.Chart(acc).mark_text(align='left',fontSize=15).encode(text='CatalogNumber:O').transform_filter(its)
            ll = alt.Chart(pd.DataFrame({'Date': [pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True)]})).mark_rule().encode(x = 'Date:T')
            chart=c1|((c2+c2.mark_circle(color="#F57F17"))+c3+c3.mark_circle(color='#42A5F5')+c4+c4.mark_circle(color='#E91E63')+ll) & c41
            print("PLOT Contribution!!")
            return chart.to_json()
    def cort(df,l2fc,fci,ski,cc):
        if not df.empty:
            print(df.info())
            print("STARTED CORR CALCULATION!!")
            df1=df[df['CatalogNumber'].isin(cc[:int(ski/2)])]
            df1=df1[['IBP Level 5','CatalogNumber','firstofmonth','`Act Orders Rev',l2fc]].copy()
            df1['firstofmonth']=pd.to_datetime(df1['firstofmonth'])
            df2=df1[df1['firstofmonth']<=pd.Timestamp.today()-pd.offsets.MonthBegin(2)]
            df2=df2.sort_values(by='`Act Orders Rev',ascending=False)
            df2=df2.pivot(columns='CatalogNumber',index='firstofmonth',values='`Act Orders Rev')
            df3=df2.corr()
            #print("CORR DONE !!")
            for i in range(len(df3)):
                for j in range(i):
                    df3.iloc[i][j]=0
            df3=df3.melt(ignore_index=False)
            print("MELT!!")
            df3=df3[df3['value']!=0]
            df3=df3.rename(columns={'value':'Correlation','CatalogNumber':'CatalogNumber1'})
            fc=df1[df1['firstofmonth']>pd.Timestamp.today()-pd.offsets.MonthBegin(2)]             
            df3=df3.reset_index()
            df4=df3[(abs(df3['Correlation'])>=.93) & (df3['CatalogNumber']!=df3['CatalogNumber1'])]
            chl=[]
            #print("PLOTTING !!!  ",len(df4))
            for i,dat in enumerate(df4.iterrows()):
                c1,c2,c3,c4='','','',''
                tdf=df1[df1['firstofmonth']<=pd.Timestamp.today()-pd.offsets.MonthBegin(2)]  
                tdf1=tdf[tdf['CatalogNumber']==dat[1][0]].sort_values('firstofmonth')
                tdf2=tdf[tdf['CatalogNumber']==dat[1][1]].sort_values('firstofmonth')
                fc1=fc[fc['CatalogNumber']==dat[1][0]].sort_values('firstofmonth')
                fc2=fc[fc['CatalogNumber']==dat[1][1]].sort_values('firstofmonth')
                c1=alt.Chart(tdf1,title=f'{dat[1][0]} vs {dat[1][1]}').mark_line(color='#E91E63').encode(x='firstofmonth', y='`Act Orders Rev',opacity=alt.value(0.75),tooltip=['firstofmonth','sum(`Act Orders Rev):Q','CatalogNumber'])
                c2=alt.Chart(tdf2,).mark_line(color='#42A5F5').encode(x='firstofmonth', y='`Act Orders Rev',opacity=alt.value(0.75),tooltip=['firstofmonth','sum(`Act Orders Rev):Q','CatalogNumber'])
                c3=alt.Chart(fc1).mark_line(color='#E91E63').encode(x='firstofmonth', y=alt.Y(l2fc,'sum',title='L2 '+fci), opacity=alt.value(0.75),tooltip=['firstofmonth',l2fc,'CatalogNumber'])
                c4=alt.Chart(fc2).mark_line(color='#42A5F5').encode(x='firstofmonth', y=alt.X(l2fc,'sum',title='L2 '+fci), opacity=alt.value(0.75),tooltip=['firstofmonth',l2fc,'CatalogNumber'])
                chl.append(c1+c1.mark_circle(color='#E91E63')+c2+c2.mark_circle(color='#42A5F5')+c3+c3.mark_circle(color='#E91E63')+c4+c4.mark_circle(color='#42A5F5'))
            print('PLOT Correlation!!')
            return alt.concat(*chl, columns=4).to_json()
    def covt(df,cc):
        if not df.empty:
            #cc=df.groupby('CatalogNumber').sum(numeric_only=True)[['`Act Orders Rev']].sort_values(ascending=False,by='`Act Orders Rev')[:300].index
            tcv=pd.DataFrame()
            tcv['cvar']=df.groupby('CatalogNumber')['`Act Orders Rev'].std()/df.groupby('CatalogNumber')['`Act Orders Rev'].mean()
            cv=df.merge(tcv,on='CatalogNumber')
            cv=cv[cv['CatalogNumber'].isin(cc)]
            cv.sort_values('firstofmonth',ascending=False,inplace=True)
            cv['err']=abs(cv['`Act Orders Rev']-cv[l2fc])/cv['`Act Orders Rev']
            cv['acc']=1-cv['err']
            cv['acc']=cv['acc'].clip(0,None)
            cv['l1macc']=cv.groupby('CatalogNumber')['acc'].shift(1)
            cv['l2macc']=cv.groupby('CatalogNumber')['acc'].shift(2)
            cv['l1macc']=cv['l1macc'].clip(0,None)
            cv['l2macc']=cv['l2macc'].clip(0,None)
            cv['3macc']=cv[['acc','l1macc','l2macc']].sum(axis=1)/3 
            its1=alt.selection_point(fields=['CatalogNumber'],nearest=True)
            f1=alt.Chart(cv[cv['firstofmonth']==pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True)]).mark_circle().encode(
                x=alt.X('mean(cvar):Q'),y=alt.Y('mean(3macc):Q',scale=alt.Scale(type="pow",exponent=0.4)),size=alt.Size('`Act Orders Rev:Q', scale=alt.Scale(range=[100,700])),tooltip=['CatalogNumber:O','IBP Level5:O']
                ,opacity=alt.condition(its1, alt.value(.8), alt.value(0.08))).properties(height=400,width=700).add_params(its1)
            f2=alt.Chart(cv).mark_line().encode(x='firstofmonth:T',y='sum(`Act Orders Rev):Q',tooltip=['firstofmonth','sum(`Act Orders Rev):Q']).properties(height=390,width=500).transform_filter(its1)
            f3=alt.Chart(cv).mark_line(color='red').encode(x='firstofmonth:T',y=alt.Y(l2fc,'sum',title='L2 '+fci),tooltip=['firstofmonth',f'sum({l2fc}):Q']).transform_filter(its1)
            f4=alt.Chart(cv).mark_line(color='green').encode(x='firstofmonth:T',y=alt.Y(l0fc,'sum',title='L0 '+fci),tooltip=['firstofmonth',f'sum({l0fc}):Q']).transform_filter(its1)
            ll = alt.Chart(pd.DataFrame({'Date': [pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True)]})).mark_rule().encode(x = 'Date:T')
            print("PLOT Covariance !!!")
            return (f1|((f2+f2.mark_circle())+f3+f3.mark_circle(color='red')+f4+f4.mark_circle()+ll)).to_json()
    def acct(df,cc):
        if not df.empty:
            #cc=df.groupby('CatalogNumber').sum(numeric_only=True)[['`Act Orders Rev']].sort_values(ascending=False,by='`Act Orders Rev')[:300].index
            acc=df.copy()
            acc['L2 Abs Var']=abs(acc['`Act Orders Rev']-acc[l2fc])
            acc['L2 Acc']=1-acc['L2 Abs Var']/acc['`Act Orders Rev']
            acc.loc[acc['`Act Orders Rev']==0,'L2 Acc']=1
            acc['L2 Acc']=acc['L2 Acc'].clip(0,None)
            acc2=acc.sort_values(['CatalogNumber','firstofmonth']).reset_index()
            acc2['Decrease']=acc2['L2 Acc'].diff()
            acc2['Per Dec']=acc2['L2 Acc'].pct_change()
            acc3=acc2[acc2['firstofmonth']==pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True)]
            acc3=acc3[acc3['CatalogNumber'].isin(cc[:220])]
            acc3=acc3[acc3['Decrease']<0].sort_values('Decrease')
            its2=alt.selection_point(fields=['CatalogNumber'])
            f5=alt.Chart(acc3).mark_bar().encode(
                x=alt.X('CatalogNumber:O',sort='y'),y=alt.Y('mean(Decrease):Q'),tooltip=['CatalogNumber:O','IBP Level 5:O']
                ,opacity=alt.condition(its2, alt.value(.8), alt.value(0.08))).properties(height=390,width=600).add_params(its2)
            f6=alt.Chart(acc2).mark_line().encode(x='firstofmonth:T',y='sum(`Act Orders Rev):Q',tooltip=['firstofmonth','sum(`Act Orders Rev):Q']).properties(height=390,width=500).transform_filter(its2)
            f7=alt.Chart(acc2).mark_line(color='red').encode(x='firstofmonth:T',y=f'sum({l2fc}):Q',tooltip=['firstofmonth',f'sum({l2fc}):Q']).transform_filter(its2)
            c51=alt.Chart(acc).mark_text(align='left',fontSize=15).encode(text='CatalogNumber:O').transform_filter(its2)
            ll = alt.Chart(pd.DataFrame({'Date': [pd.Timestamp.today()-pd.offsets.MonthBegin(2,normalize=True)]})).mark_rule().encode(x = 'Date:T')
            print('PLOT Accuracy!!')
            return ((f5|((f6+f6.mark_circle())+f7+f7.mark_circle(color='red')+ll) & c51)).to_json()

    return html.div(html.div({"class_name":"ui top attached tabular menu"},
                    html.div({"class_name":"item","data-tab":"Correlation"}, "Correlation"),
                    html.div({"class_name":"item","data-tab":"Contribution"},"Contribution"),
                    html.div({"class_name":"item","data-tab":"COV"},"COV"),
                    html.div({"class_name":"item","data-tab":"Accuracy"},"Accuracy"),
                    html.div({"class_name":"item","data-tab":"Change"},"Change")),
                    html.div({"class_name":"ui tab", "data-tab":"Correlation"},
                             html.div({"id":"vis1"}),
                             html.script({"language":"javascript"},f'''vegaEmbed('#vis1', {cort(df,l2fc,fci,ski,cc)});''')),
                    html.div({"class_name":"ui tab", "data-tab":"Contribution"},
                             html.div({"id":"vis"}),
                             html.script({"language":"javascript"},f'''vegaEmbed('#vis', {cont(df,l2fc,l0fc,fci)});''')),
                    html.div({"class_name":"ui tab", "data-tab":"COV"},
                             html.div({"id":"vis2"}),
                             html.script({"language":"javascript"},f'''vegaEmbed('#vis2', {covt(df,cc)});''')),
                    html.div({"class_name":"ui tab", "data-tab":"Accuracy"},
                             html.div({"id":"vis3"}),
                             html.script({"language":"javascript"},f'''vegaEmbed('#vis3', {acct(df,cc)});''')),
                    html.div({"class_name":"ui tab", "data-tab":"Change"},"gfdfsfsdfs"))

@component
def App():
    fr,set_fri=use_state("CMF")
    co,set_coi=use_state("INDIA")
    fci,set_fci=use_state("Stat Fcst")
    ski,set_ski=use_state(80)
    dfi,set_dfi=use_state(pd.DataFrame())
    uni,set_uni=use_state('')
    pwi,set_pwi=use_state('')
    pi,set_pi=use_state("password")
    sl,set_sl=use_state(" slash")
    if not dfi.empty:
        cc=dfi.groupby('CatalogNumber').sum(numeric_only=True)[['`Act Orders Rev']].sort_values(ascending=False,by='`Act Orders Rev')[:ski].index
    else:
        cc=''
    try:
        with open('config.json') as json_file:
            fdata = json.load(json_file)
            un = fdata.get('username')
            pp = fdata.get('password')
            set_uni(un)
            set_pwi(pp)
    except:
        pass

    if fci=='Stat Fcst':
        l2fc='L2 Stat Final Rev'
        l0fc='`Fcst Stat Final Rev'
    else:
        l2fc='L2 DF Final Rev'
        l0fc='`Fcst DF Final Rev'

    def sabf(e):
        cred={'username':uni,'password':pwi}
        with open('config.json', 'w+') as outfile:
            outfile.write(json.dumps(cred))
    def frf(e):
        set_fri(e["target"]["value"])
    def cof(e):
        set_coi(e["target"]["value"])
    def fcf(e):
        set_fci(e["target"]["value"])
    def lpr(e):
        print(co,fr)
        df=pd.read_parquet(f'{[co]}-{[fr]}.parquet')
        set_dfi(df)
        print(dfi)
    def myf(e):
        if pi=="password":
            set_pi("text")
            set_sl('')
        else:
            set_pi("password")
            set_sl(" slash")
    def enbf(e):
        df=data(co,[fr],uni,pwi)
        df.to_parquet(f'{[co]}-{[fr]}.parquet')

    k=html.div(html.div({"class_name":"ui"},
               html.div({"class_name":"ui styled fluid accordion"},
               html.div({"class_name":"title"}, html.i({"class_name":"dropdown icon"}),"Credentials"),
               html.div({"class_name":"ui form content"},
                         html.div({"class_name":"ui three fields transition"},
                                  html.div({"class_name":"field"},
                        html.input({"placeholder":"User Name","class_name":"ui input","value":uni,"on_change":lambda e: set_uni(e['target']['value'])})),
                        html.div({"class_name":"field"},
                        html.input({"placeholder":"Password","type":pi,"class_name":"ui input attached field","id":"myInput","value":pwi,"on_change":lambda e: set_pwi(e['target']['value'])})),
                        html.i({"on_click":myf,"class":"eye attached icon"+sl,"style":{"margin-left": "4px", "cursor": "pointer"},"id":"togglePassword"}),
                        html.div({"class_name":"field"},
                        html.button({"on_click":sabf,"class_name":"ui primary button field"},"Save"))))),
                        html.div({"class_name":"ui form basic segment"},
                         html.div({"class_name":"six fields"},
                                  html.div({"class_name":"field"},
                                  html.select({"class_name":"ui selection dropdown","value":fci,"on_change":fcf},
                                           html.i({"class_name":"dropdown icon"}),
                                  html.option({"class_name":"item","value":"Stat Fcst"},'Stat Fcst'),
                                  html.option({"class_name":"item","value":"DF Fcst"},'DF Fcst')
                                  )),
                                  html.div({"class_name":"field"},
                                  html.select({"class_name":"ui fluid search dropdown","multiple":"true","value":fr,"on_change":frf},
                                           html.div({"class_name":"ui text"},"Franchise"),
                                           html.i({"class_name":"dropdown icon"}),
                                  [html.option({"class_name":"item","value":i},i) for i in fran],
                                  )),
                                  html.div({"class_name":"field"},
                                  html.select({"class_name":"ui selection dropdown","value":co,"on_change":cof},
                                           html.div({"class_name":"ui text"},"Country"),
                                           html.i({"class_name":"dropdown icon"}),
                                    [html.option({"class_name":"item","value":i},i) for i in coun],
                                  )),
                                  html.div({"class_name":"field"},
                                  html.input({"class_name":"ui text","type":"number","value":ski,"on_change":lambda e: set_ski(e['target']['value'])}),
                                  ),
                                  html.div({"class_name":"field"},
                                  html.button({"class_name":"ui primary button", "on_click":enbf},"Get Envision"),
                                  html.button({"class_name":"ui primary button", "on_click":lpr},"Load Local")
                                  ))),
                                  tchart(dfi,l2fc,l0fc,fci,ski,cc),
                                html.script({"language":"javascript"},"$('.ui.accordion').accordion();$('.ui.dropdown').dropdown();$('.tabular.menu .item').tab();")))
    return k

#run(App)
app = Sanic("MyHelloWorldApp")
configure(app,App,Options(head=headv))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")