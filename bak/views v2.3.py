from django.shortcuts import render,get_object_or_404
from .models import Product,So,Plan,Line,Speed,Material,BOM
from .admin import SOResource
from django.forms import modelformset_factory,inlineformset_factory,formset_factory
from .tables import SoFilter,PlanFilter,SoTable,PlanTable
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .forms import PlanForm,LineForm,DateInput,PlanForm1,SoForm2
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from django.views.generic import ListView,FormView,UpdateView
from django.views.generic.edit import FormMixin
import django_tables2 as tables
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Div,Field,Fieldset,HTML,ButtonHolder,Row
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .custom_layout_object import Formset
import holoviews as hv
from django_pandas.io import read_frame
import dtale
from django.shortcuts import redirect


# Create your views here.
def index(request):
    model = So
    return render(request,'app1/base.html')

soinlineformset =  inlineformset_factory(So, Plan,form=PlanForm1,widgets={'date': DateInput()},extra=1,can_delete=True)
class SoForm1(UpdateView):
    model = So
    #form_class = SoForm
    template_name = 'app1/formmixin.html'
    fields=('so','so_date','so_del_date','closed','code','customer','qty','act_disp_qty','act_disp_date')
    def get_success_url(self):
        return reverse_lazy('solist')
    def get_context_data(self, **kwargs):
        data = super(SoForm1, self).get_context_data(**kwargs)
        if self.request.POST:
            data['plan'] = soinlineformset(self.request.POST,instance=self.object)
        else:
            data['plan'] = soinlineformset(instance=self.object)
        data['helper'] = SoForm1.get_form(self).helper
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        self.object = form.save()
        plan = context['plan']
        with transaction.atomic():
            self.object = form.save()
            if plan.is_valid():
                plan.instance = self.object
                #print(plan)
                plan.save()
        return super(SoForm1, self).form_valid(form)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_tag = True
        #form.helper.form_class = 'form-horizontal'
        form.helper.layout = Layout(
                Row(
                        Field('so'),
                        Field('so_date'),
                        Field('customer'),
                        'so_del_date','closed'),
                    Row(    
                        Field('qty'),
                        Field('act_disp_qty'),
                        Field('act_disp_date'),
                        'code',
                        ),
                    Row(
                        Fieldset('Add Plan',
                        Formset('plan')),
                    )
                )
        #form.helper.field_class = 'col-md-4'
        #form.helper.template = 'bootstrap4/table_inline_formset.html
        form.helper.form_method = 'post'
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        #form.fields['act_disp_date'].widget = DateInput()
        return form

class SoList(SingleTableMixin,FilterView):
    model = So
    table_class = SoTable
    table_data = So.objects.filter(closed=0)
    template_name = 'app1/list.html'
    filterset_class = SoFilter

class WPList(SingleTableMixin,FilterView):
    model = So
    table_class = SoTable
    #pp= Plan.objects.filter(date__isnull=True).values_list('so_id', flat=True)
    table_data = So.objects.filter(closed=0).filter(plan__date__isnull=True)
    template_name = 'app1/list.html'
    filterset_class = SoFilter

class PlanList(SingleTableMixin,FilterView):
    model = Plan
    table_class = PlanTable
    table_data = So.objects.filter(closed=0)
    template_name = 'app1/list.html'
    filterset_class = PlanFilter

class SpeedList(SingleTableMixin,FilterView):
    model = Speed
    template_name = 'app1/list.html'

class ProductList(SingleTableMixin,FilterView):
    model = Product
    template_name = 'app1/list.html'

class MaterialList(SingleTableMixin,FilterView):
    model = Material
    template_name = 'app1/list.html'

class BOMList(SingleTableMixin,FilterView):
    model = BOM
    template_name = 'app1/list.html'

def export(request):
    so_resource = SOResource()
    dataset = so_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="so.csv"'
    return response

def SoView(request):
    soformset = modelformset_factory(So,form=SoForm2,extra=5)
    helper = SoForm2().helper
    #helper.add_input(Submit('submit', 'Submit'))
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
        formset = soformset(request.POST)
        if formset.is_valid():
            print(formset.save())
        else:
            formset = soformset(queryset=page_query.order_by('id'))
    else:
        formset = soformset(queryset=page_query.order_by('id'))
    context = {'object': objects, 'formset': formset, 'helper': helper }
    return render(request,'app1/so_form.html',context)

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
    pp = Plan.objects.values()
    df = pd.DataFrame(pp)
    print(df)
    ss = So.objects.values('id','so','so_del_date','code','qty','closed')
    df1 = pd.DataFrame(ss)
    df1 = df1.loc[df1.closed==0]
    df = pd.merge(df1,df,how='left',left_on='id',right_on='so_id')
    df = df[df.date.notnull()]
    sp = Speed.objects.values()
    df2 = pd.DataFrame(sp)
    df = pd.merge(df,df2,how='left',left_on=['code','line_id'],right_on=['code_id','line_id'])
    pr = Product.objects.values('code','case_size')
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code'],right_on=['code'])
    #print(df.columns)
    kk = px.bar(data_frame=df, x='line_id', y=(df['qty']*df['case_size'])/(df['speed']*480.0*0.7), opacity=0.8,facet_row=df['date'])
    fig = go.Figure(data=kk)
    #fig.update_xaxes(tickvals=df['line_id'].unique())
    graph = fig.to_html(full_html=False,default_height=900,config={'editable':False,'edits':{'shapePosition':True}})
    context = {'graph': graph}
    return render(request, "app1/plotly.html", context)

def sopivot(request):
    ss = So.objects.values()
    df = pd.DataFrame(ss)
    pr = Product.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code_id'],right_on=['code'])
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

def sopivot1(request):
    ss = So.objects.values()
    df = pd.DataFrame(ss)
    pr = Product.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code_id'],right_on=['code'])
    df.pop('rate')
    df.pop('micro')
    df.pop('carton')
    df.pop('act_disp_date')
    df = df.to_json(orient='values',date_format='iso')
    context = {'df': df}
    return render(request, "app1/org.html", context)

def planpivot(request):
    pp = Plan.objects.values()
    df = pd.DataFrame(pp)
    ss = So.objects.values()
    df1 = pd.DataFrame(ss)
    df1 = df1.loc[df1.closed==0]
    df = pd.merge(df1,df,how='left',left_on='id',right_on='so_id')
    #df = df[df.date.notnull()]
    ll = Line.objects.values()
    df2 = pd.DataFrame(ll)
    df = pd.merge(df,df2,how='left',left_on=['line_id'],right_on=['line'])
    pr = Product.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code_id'],right_on=['code'])
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

def holoview(request):
    pp = Plan.objects.values()
    df = pd.DataFrame(pp)
    ss = So.objects.values('id','so','so_del_date','code','qty','closed')
    df1 = pd.DataFrame(ss)
    df1 = df1.loc[df1.closed==0]
    df = pd.merge(df1,df,how='left',left_on='id',right_on='so_id')
    df = df[df.date.notnull()]
    sp = Speed.objects.values()
    df2 = pd.DataFrame(sp)
    df = pd.merge(df,df2,how='left',left_on=['code','line_id'],right_on=['code_id','line_id'])
    pr = Product.objects.values('code','case_size')
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code'],right_on=['code'])
    #print(df.columns)
    kk = hv.Bars(df, kdims='line_id', vdims=['qty'],facet_row='date')
    graph = hv.renderer('plotly').static_html(kk)
    #fig.update_xaxes(matches='x')
    #graph = fig.to_html(full_html=False,default_height=900,config={'editable':False,'edits':{'shapePosition':True}})
    context = {'graph': graph}
    return render(request, "app1/plotly.html", context)


from dtale.utils import build_url
from dtale.views import startup
import dtale.app as dtale_app

def sopivot2(request):
    qs = So.objects.all()
    ff=[f.name for f in So._meta.get_fields()]
    ff.extend(['code__'+k.name for k in Product._meta.get_fields()])
    #print(ff)
    ff.remove('code__so')
    #print(ff)
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    #df = df.to_html(table_id="input",index=False)
    #context = {'df': df}
    #return render(request, "app1/pivot.html", context)
    d = dtale.show(df)
    #d.open_browser()
    response = redirect(d._main_url)
    return response
    #context = {'context1': 'd._main_url'}
    #print(dtale.show(df))
    #return render(request, url)