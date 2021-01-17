from django.shortcuts import render,get_object_or_404
from .models import *
from .admin import SOResource
from django.forms import modelformset_factory,inlineformset_factory,formset_factory
from .tables import *
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .forms import *
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from django.views.generic import ListView,FormView,UpdateView,CreateView,DetailView
from django.views.generic.edit import FormMixin,DeletionMixin
import django_tables2 as tables
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,Layout,Div,Field,Fieldset,HTML,ButtonHolder,Row,Button
from crispy_forms.bootstrap import InlineField,FormActions
from django.urls import reverse, reverse_lazy
from django.db import transaction
from .custom_layout_object import Formset
from django_pandas.io import read_frame
import dtale
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django_tables2.export.export import TableExport
from django.views.generic.dates import MonthArchiveView
from django import forms
from django_select2.forms import Select2Widget,ModelSelect2Widget
from datetime import datetime
from django_tables2.export.views import ExportMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.db.models import Sum,Count
from django_tables2.config import RequestConfig
from django.contrib import messages
from django.db.models import F
from django.db.models import Subquery, OuterRef
from dal import autocomplete

# Create your views here.
def index(request):
    model = So
    return render(request,'app1/base.html')

soinlineformset =  inlineformset_factory(So, Plan,form=PlanForm,widgets={'date': DateInput()},extra=5,can_delete=True)

class ProductWidget(ModelSelect2Widget):
    queryset = Product.objects.all()
    search_fields = [
        'code__icontains',
        'desc__icontains',
    ]
    
class MaterialWidget(ModelSelect2Widget):
    queryset = Material.objects.all()
    search_fields = [
        'code__icontains',
        'desc__icontains',
    ]

class OpenSoWidget(ModelSelect2Widget):
    queryset = So.objects.filter(closed=0)
    search_fields = [
        'so__icontains',
        'fgcode__code__icontains',
        'fgcode__desc__icontains',
    ]

@permission_required("app1.add_so",login_url='/accounts/login/')   
def SoCreate(request):
    SoFormSet = modelformset_factory(So, fields=('so','fgcode','so_date','so_del_date','closed','customer','so_qty'), extra=9,
					widgets={'fgcode': autocomplete.ModelSelect2(url='product-autocomplete'),'so_date': DateInput(),'so_del_date': DateInput()})
    helper = SoForm.helper
    if request.method == 'POST':
        formset = SoFormSet(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = SoFormSet(queryset=So.objects.none())
    return render(request, 'app1/create_form.html', {'formset': formset,'helper':helper})

@permission_required("app1.add_line",login_url='/accounts/login/')  
def LineCreate(request):
    LineFormset = modelformset_factory(Line,fields=('__all__'))
    helper = LineForm.helper
    if request.method == 'POST':
        formset = LineFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            formset = LineFormset(queryset=Line.objects.none())
    else:
        formset = LineFormset(queryset=Line.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.add_product",login_url='/accounts/login/')     
def ProductCreate(request):
    ProductFormset = modelformset_factory(Product,exclude=('des_code','cust_code','pts','cbm','gr_wt'),extra=5)
    helper = ProductForm.helper
    if request.method == 'POST':
        formset = ProductFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            formset = ProductFormsetFormset(queryset=Product.objects.none())
    else:
        formset = ProductFormset(queryset=Product.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.add_speed",login_url='/accounts/login/')  
def SpeedCreate(request):
    SpeedFormset = modelformset_factory(Speed,fields=('__all__'),extra=5,widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete')})
    helper = SpeedForm.helper
    if request.method == 'POST':
        formset = SpeedFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            formset = SpeedFormset(queryset=Speed.objects.none())
    else:
        formset = SpeedFormset(queryset=Speed.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.add_production",login_url='/accounts/login/')  
def ProductionCreate(request):
    ProductionFormset = modelformset_factory(Production,fields=('__all__'),extra=10,widgets={'date':DateInput,'so': autocomplete.ModelSelect2(url='openso-autocomplete')})
    helper = ProductionForm.helper
    if request.method == 'POST':
        formset = ProductionFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = ProductionFormset(queryset=Production.objects.none())
    else:
        formset = ProductionFormset(queryset=Production.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.add_dispatch",login_url='/accounts/login/')  
def DispatchCreate(request):
    DispatchFormset = modelformset_factory(Dispatch,fields=('__all__'),extra=8,widgets={'dispatch_date':DateInput,'so':autocomplete.ModelSelect2(url='openso-autocomplete')})
    helper = DispatchForm.helper
    if request.method == 'POST':
        formset = DispatchFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = DispatchFormset(queryset=Dispatch.objects.none())
    else:
        formset = DispatchFormset(queryset=Dispatch.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.add_customer",login_url='/accounts/login/')  
def CustomerCreate(request):
    CustomerFormset = modelformset_factory(Customer,fields=('__all__'),extra=2)
    helper = CustomerForm.helper
    if request.method == 'POST':
        formset = CustomerFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = CustomerFormset(queryset=Customer.objects.none())
    else:
        formset = CustomerFormset(queryset=Customer.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)
    
@permission_required("app1.add_bom",login_url='/accounts/login/')  
def BOMCreate(request):
    BOMFormset = modelformset_factory(BOM,fields=('__all__'),extra=7,widgets={'fgcode':autocomplete.ModelSelect2(url='product-autocomplete'),'material_code':autocomplete.ModelSelect2(url='material-autocomplete')})
    helper = BOMForm.helper
    if request.method == 'POST':
        formset = BOMFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            formset = BOMFormset(queryset=BOM.objects.none())
    else:
        formset = BOMFormset(queryset=BOM.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.add_material",login_url='/accounts/login/')  
def MaterialCreate(request):
    MaterialFormset = modelformset_factory(Material,fields=('__all__'),extra=7,widgets={'material_code':autocomplete.ModelSelect2(url='material-autocomplete')})
    helper = MaterialForm.helper
    if request.method == 'POST':
        formset = MaterialFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = MaterialFormset(queryset=Material.objects.none())
    else:
        formset = MaterialFormset(queryset=Material.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.change_so",login_url='/accounts/login/')  
def SoUpdate(request):
    fields=('fgcode','so','so_date','so_del_date','commit_disp_date','so_qty','closed','remarks')
    SoUpFormset = modelformset_factory(So,fields=fields,widgets={'fgcode':autocomplete.ModelSelect2(url='product-autocomplete')},can_delete=True)
    helper = SoForm1.helper
    f = SoFilter(request.GET, queryset=So.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = SoUpFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
        #if formset.is_valid():
                form.save()
            if not form.is_valid():
                print(form.errors)
                messages.error(request, "Please correct the errors below and resubmit.")
            else:
                formset = SoUpFormset(queryset=page_query)
    else:
        formset = SoUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)

@permission_required("app1.change_product",login_url='/accounts/login/')  
def ProductUpdate(request):
    ProductUpFormset = modelformset_factory(Product,exclude=('cust_code','pts','cbm','plant','des_code','customer','nt_wt','gr_wt','case_size','bulk_code'))
    helper = ProductForm.helper
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = ProductUpFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = ProductUpFormset(queryset=page_query)
    else:
        formset = ProductUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)

@permission_required("app1.change_dispatch",login_url='/accounts/login/')  
def DispatchUpdate(request):
    DispatchUpFormset = modelformset_factory(Dispatch,fields=('__all__'))
    helper = DispatchForm.helper
    f = DispatchFilter(request.GET, queryset=Dispatch.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = DispatchUpFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = DispatchUpFormset(queryset=page_query)
    else:
        formset = DispatchUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)

@permission_required("app1.change_dispatch",login_url='/accounts/login/')  
def ProductionUpdate(request):
    ProductionUpFormset = modelformset_factory(Production,fields=('__all__'),can_delete=True,extra=0)
    helper = ProductionForm.helper
    f = ProductionFilter(request.GET, queryset=Production.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = ProductionUpFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            formset = ProductionUpFormset(queryset=page_query)
    else:
        formset = ProductionUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)

class SoDetail1(UpdateView):
    model = So
    #form_class = SoForm
    template_name = 'app1/formmixin.html'
    fields=('id','so','so_date','so_del_date','closed','fgcode','customer','so_qty','act_disp_qty','act_disp_date')
    def get_success_url(self):
        return reverse_lazy('solist')
    def get_context_data(self, **kwargs):
        data = super(SoDetail, self).get_context_data(**kwargs)
        if self.request.POST:
            data['plan'] = soinlineformset(self.request.POST,instance=self.object)
        else:
            data['plan'] = soinlineformset(instance=self.object)
        data['helper'] = SoDetail.get_form(self).helper
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
        return super(SoDetail, self).form_valid(form)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_tag = True
        #form.helper.form_class = 'form-horizontal'
        form.helper.layout = Layout(
                Row(
                        Field('id'),
                        Field('so'),
                        Field('so_date'),
                        Field('customer'),
                        'so_del_date','closed'),
                    Row(    
                        Field('so_qty'),
                        Field('act_disp_qty'),
                        Field('act_disp_date'),
                        'fgcode',
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

     
class ProductDetail(UpdateView):
    model = Product
    #table_class = ProductTable
    #form_class = ProductForm
    template_name = 'app1/form.html'
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('productlist')
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        context['helper'] = ProductDetail.get_form(self).helper
        context['form'] = ProductForm(instance=self.object) 
        return context
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.label_class = 'mt-3 mr-3'
        form.helper.field_class = 'mt-3 mr-3'
        form.helper.form_method = 'post'
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        return form

class ProductionDetail(UpdateView):
    model = Production
    template_name = 'app1/form.html'
    #fields='__all__'
    form_class = ProductionForm1
    def get_success_url(self):
        return reverse_lazy('productionlist')
    '''
    def get_context_data(self, **kwargs):
        context = super(ProductionDetail, self).get_context_data(**kwargs)
        context['helper'] = ProductionDetail.get_form(self).helper
        context['form'] = ProductionForm(instance=self.object) 
        return context
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.label_class = 'mt-3 mr-3'
        form.helper.field_class = 'mt-3 mr-3'
        form.helper.form_method = 'post'
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        return form'''

class DispatchDetail(UpdateView):
    model = Dispatch
    template_name = 'app1/form.html'
    #fields='__all__'
    form_class = DispatchForm1
    def get_success_url(self):
        return reverse_lazy('dispatchlist')
        
def BOMDetail(request,fgcode_id=None):
    #model = BOM
    bomformset=modelformset_factory(BOM,fields=('__all__'),can_delete=True,extra=0)
    template_name = 'app1/update_form.html'
    fields='__all__'
    helper = BOMForm.helper
    if request.method == 'POST':
        formset = bomformset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            formset = bomformset(queryset=BOM.objects.filter(fgcode_id=fgcode_id))
    else:
        formset = bomformset(queryset=BOM.objects.filter(fgcode_id=fgcode_id))
    context = {'formset': formset,'helper':helper}
    print(BOM.objects.filter(fgcode=fgcode_id))
    return render(request,'app1/update_form.html',context)

class SoDetail(UpdateView):
    model = So
    template_name = 'app1/form.html'
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('solist')
    def get_context_data(self, **kwargs):
        context = super(SoDetail, self).get_context_data(**kwargs)
        context['helper'] = SoDetail.get_form(self).helper
        context['form'] = SoForm(instance=self.object) 
        return context
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.label_class = 'mt-3 mr-3'
        form.helper.field_class = 'mt-3 mr-3'
        form.helper.form_method = 'post'
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        return form

class MaterialDetail(DeletionMixin,UpdateView):
    model = Material
    template_name = 'app1/form.html'
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('materiallist')
    def get_context_data(self, **kwargs):
        context = super(MaterialDetail, self).get_context_data(**kwargs)
        context['helper'] = MaterialDetail.get_form(self).helper
        context['form'] = MaterialForm(instance=self.object) 
        return context
    # Working delete Button
    #def post(self, request, pk):
    #    if 'confirm_delete' in self.request.POST:
    #        return self.delete(request)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.label_class = 'mt-3 mr-3'
        form.helper.field_class = 'mt-3 mr-3'
        form.helper.form_method = 'post'
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        return form

class SoList(SingleTableMixin,ExportMixin,FilterView):
    model = So
    paginate_by = 20
    table_class = SoTable
    #table.paginate(per_page=25)
    #table_data = So.objects.filter(closed=0)
    template_name = 'app1/list.html'
    filterset_class = SoFilter

class CustomerList(SingleTableMixin,ExportMixin,FilterView):
    model = Customer
    paginate_by = 20
    table_class = CustomerTable
    #table.paginate(per_page=25)
    #table_data = So.objects.filter(closed=0)
    template_name = 'app1/list.html'
    #filterset_class = SoFilter
    #SingleTableMixin.table_pagination = False

class WPList(SingleTableMixin,FilterView):
    model = So
    #table = SoTable(So.objects.filter(closed=0).filter(plan__date__isnull=True))
    #pp= Plan.objects.filter(date__isnull=True).values_list('so_id', flat=True)
    #table_data = So.objects.filter(closed=0).filter(plan__date__isnull=True)
    template_name = 'app1/list.html'
    filterset_class = SoFilter

class PlanList(SingleTableMixin,FilterView):
    model = Plan
    table_class = PlanTable
    #table_data = So.objects.filter(closed=0)
    template_name = 'app1/list.html'
    filterset_class = PlanFilter

class SpeedList(SingleTableMixin,FilterView):
    model = Speed
    template_name = 'app1/list.html'

class ProductList(SingleTableMixin,ExportMixin,FilterView):
    model = Product
    template_name = 'app1/list.html'
    table_class = ProductTable
    filterset_class = ProductFilter


class MaterialList(SingleTableMixin,ExportMixin,FilterView):
    model = Material
    template_name = 'app1/list.html'
    table_class = MaterialTable
    filterset_class = MaterialFilter

class BOMList(SingleTableMixin,ExportMixin,FilterView):
    model = BOM
    template_name = 'app1/list.html'
    table_class = BOMTable
    filterset_class = BOMFilter
    
class ProductionList(SingleTableMixin,ExportMixin,FilterView):
    model = Production
    template_name = 'app1/list.html'
    filterset_class = ProductionFilter
    table_class = ProductionTable

class DispatchList(SingleTableMixin,ExportMixin,FilterView):
    model = Dispatch
    template_name = 'app1/list.html'
    table_class = DispatchTable
    filterset_class = DispatchFilter


def visualization(request):
    pp = Plan.objects.values()
    df = pd.DataFrame(pp)
    ss = So.objects.values('id','so','so_del_date','fgcode','so_qty','closed')
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
    kk = px.bar(data_frame=df, x='line_id', y=(df['so_qty']*df['case_size'])/(df['speed']*480.0*0.7), opacity=0.8,facet_row=df['date'])
    fig = go.Figure(data=kk)
    graph = fig.to_html(full_html=False,default_height=900,config={'editable':False,'edits':{'shapePosition':True}})
    context = {'graph': graph}
    return render(request, "app1/plotly.html", context)

def sopivot(request):
    ss = So.objects.values()
    df = pd.DataFrame(ss)
    pr = Product.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['fgcode_id'],right_on=['id'])
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

def matreqpivot(request):
    ss = So.objects.values()
    df = pd.DataFrame(ss)
    bm = BOM.objects.values()
    df1 = pd.DataFrame(bm)
    print(df1.columns)
    df = pd.merge(df,df1,how='left',left_on=['fgcode_id'],right_on=['bom_id__fgcode'])
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

def prodpivot(request):
    ss = Production.objects.values()
    df = pd.DataFrame(ss)
    ps = So.objects.values()
    df2 = pd.DataFrame(ps)
    df = pd.merge(df,df2,how='left',left_on=['so_id'],right_on=['id'])
    pr = Product.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['fgcode_id'],right_on=['id'])
    ll = Line.objects.values()
    df4 = pd.DataFrame(ll)
    df = pd.merge(df,df4,how='left',left_on=['line_id'],right_on=['id'])
    df.pop('rate')
    df.pop('micro')
    #df = df.to_json(orient='values',date_format='iso')
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

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

def sodview(request):
    qs = So.objects.all()
    ff=[f.name for f in So._meta.get_fields()]
    ff.extend(['fgcode__'+k.name for k in Product._meta.get_fields()])
    ff.remove('fgcode__so')
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    d = dtale.show(df,name='so')
    try:
        response = redirect(d._main_url)
    except:
        response = redirect('http://asus:40000/dtale/main/so')
    return response

def matreq(request):
    #qs = Material.objects.all()
    qs = Material.objects.raw('''SELECT m.id,m.code,m.desc, f.code AS fgcode,f.desc AS fdesc, SUM(s.so_qty) AS so_qty,b.qty as bqty, SUM(b.qty*s.so_qty) AS req FROM ((( app1_material m  
                                                                                              LEFT JOIN app1_bom b ON b.material_code_id=m.id)
                                                                                              LEFT JOIN app1_so s ON b.fgcode_id=s.fgcode_id)
                                                                                              LEFT JOIN app1_product f ON f.id=b.fgcode_id) WHERE s.closed=FALSE AND b.active=TRUE GROUP BY m.id,f.code,f.desc,bqty''')
    #print(qs)
    f = MaterialFilter(request.GET, queryset=qs)
    paginate_by = 25
    table = MaterialTable1(f)
    RequestConfig(request, paginate={'per_page': 25, 'page': 1}).configure(table)
    return render(request, "app1/list.html", {"table": table,"filter":f})
    
def openso(request):
    qs= So.objects.filter(closed=False).annotate(production_sum=Sum('production__prod_qty'),prod_balance=F('so_qty')-F('production_sum')
    ,dispatch_sum=Subquery(Dispatch.objects.filter(so=OuterRef('pk')).values('so').annotate(the_sum=Sum('dis_qty'),).values('the_sum')[:1]))
    f = SoFilter(request.GET, queryset=qs)
    paginate_by = 25
    table = SoTable1(f.qs)
    RequestConfig(request, paginate={'per_page': 25, 'page': 1}).configure(table)
    return render(request, "app1/list.html", {"table": table,"filter":f})