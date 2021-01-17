from django.shortcuts import render
from .models import Product,So,Plan,Line,Speed
from .admin import SOResource
from django.forms import modelformset_factory,inlineformset_factory,formset_factory
from .tables import SoTable, SoFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .forms import SoForm,PlanForm,LineForm,DateInput
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from django.db import connection
import plotly.io as pio
import numpy as np

# Create your views here.
class SoList(SingleTableMixin,FilterView):
    model = So
    table_class = SoTable
    template_name = 'app1/so_list.html'
    filterset_class = SoFilter

def so_agg(request):
    ordersrecieved = So.objects.filter(closed=False)
    return render(request,'app1/so_agg.html',{"ordersrecieved": ordersrecieved})

def export(request):
    so_resource = SOResource()
    dataset = so_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="so.csv"'
    return response

def SoView(request):
    Soformset = modelformset_factory(So,form =SoForm,extra=0)
    helper = SoForm.helper
    query = So.objects.filter(closed=0).order_by('id')
    paginator = Paginator(query, 30) # Show 10 forms per page
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects]).order_by('id')
    if request.method == 'POST':
        formset = Soformset(request.POST)
        if formset.is_valid():
            formset.save()
            formset = Soformset(queryset=page_query.order_by('id'))
        else:
            formset = Soformset(queryset=page_query.order_by('id'))
    else:
        formset = Soformset(queryset=page_query)
    context = {'object': objects, 'formset': formset, 'helper': helper}
    return render(request,'app1/so_form.html',context)
    

def SoTableView(SingleTableView):
    Soformset = modelformset_factory(So, fields=('so','so_del_date','code','qty','customer','closed'))
    form = Soformset(queryset=So.objects.filter(closed=0))
    return render(request,'app1/plan.html',{'formset':form})

def index(request):
    model = So
    return render(request,'app1/base.html')

def PlanView(request):
    PlanFormset = modelformset_factory(Plan,form = PlanForm, fields =('so','date','line'), extra=5,widgets={'date': DateInput()})
    #PlanFormset = formset_factory(PlanForm, extra=5,can_order=True)
    query = Plan.objects.all()
    helper = PlanForm.helper
    paginator = Paginator(query, 30)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects]).order_by('id')
    if request.method == 'POST':
        formset = PlanFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            formset = PlanFormset(queryset=page_query.order_by('id'))
    else:
        formset = PlanFormset(queryset=page_query.order_by('id'))
    context = {'object': objects, 'formset': formset, 'helper': helper}
    return render(request,'app1/plan.html',context)

def LineView(request):
    LineFormset = modelformset_factory(Line,form =LineForm)
    helper = LineForm.helper
    query = Line.objects.all()
    #query = qq.so_set.all(closed=0)
    paginator = Paginator(query, 30)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects]).order_by('id')
    if request.method == 'POST':
        formset = LineFormset(request.POST)
        if formset.is_valid():
            formset.save()
            formset = LineFormset(queryset=page_query.order_by('id'))
        else:
            formset = LineFormset(queryset=page_query.order_by('id'))
    else:
        formset = LineFormset(queryset=page_query)
    context = {'object': objects, 'formset': formset,'helper':helper}
    return render(request,'app1/form.html',context)

def visualization(request):
    pio.renderers.default = 'browser'
    pp = Plan.objects.values()
    df = pd.DataFrame(pp)
    ss = So.objects.values('id','so','so_del_date','code','qty','closed')
    df1 = pd.DataFrame(ss)
    df1 = df1.loc[df1.closed==0]
    df = pd.merge(df1,df,how='left',left_on='id',right_on='so_id')
    df = df[df.date.notnull()]
    sp = Speed.objects.values()
    df2 = pd.DataFrame(sp)
    kk = px.bar(x=df['line_id'], y=df['qty'], opacity=0.8,facet_row=df['date'].astype('str'))
    #fig = go.Figure(data=go.Bar(x=df['line_id'], y=df['qty'], opacity=0.8 ))
    fig = go.Figure(data=kk)
    #fig.update_layout(autosize=True)
    #print(df['qty'])
    graph = fig.to_html(full_html=False,default_height=900)
    #graph = pio.show(fig)
    context = {'graph': graph}
    return render(request, "app1/plotly.html", context)
