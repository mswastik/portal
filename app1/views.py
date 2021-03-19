from django.shortcuts import render,get_object_or_404
from .models import *
from .tables import *
from .forms import *
from .admin import SOResource
from django.forms import modelformset_factory,inlineformset_factory,formset_factory
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
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
from django_tables2.export.views import ExportMixin
from django.views.generic.dates import MonthArchiveView
from django import forms
from django_select2.forms import Select2Widget,ModelSelect2Widget
from datetime import datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum,Count
from django_tables2.config import RequestConfig
from django.db.models import F,Subquery, OuterRef
from dal import autocomplete
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.functions import Coalesce

# Create your views here.
def index(request):
    model = So
    return render(request,'app1/base.html')

soinlineformset =  inlineformset_factory(So, Plan,form=PlanForm,widgets={'date': DateInput()},extra=5,can_delete=True)
    
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
    SoFormSet = modelformset_factory(So, fields=('so','code','so_date','so_del_date','closed','customer','so_qty','rate'), extra=9,
					widgets={'code': autocomplete.ModelSelect2(url='product-autocomplete'),'so_date': DateInput(),'so_del_date': DateInput()})
    helper = SoForm.helper
    helper.field_class = 'input-group-sm form-control-sm mt-0'

    if request.method == 'POST':
        formset = SoFormSet(request.POST)
        if formset.is_valid():
            formset.save()
    else:
        formset = SoFormSet(queryset=So.objects.none())
    return render(request, 'app1/create_form.html', {'formset': formset,'helper':helper})

@permission_required("app1.add_line",login_url='/accounts/login/')  
def LineCreate(request):
    LineFormset = modelformset_factory(Line,fields=('__all__'),extra=6)
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
    BOMFormset = modelformset_factory(BOM,fields=('__all__'),extra=7,widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete'),'ccode':autocomplete.ModelSelect2(url='material-autocomplete')})
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

def WCGroupCreate(request):
    WCGroupFormset = modelformset_factory(WCGroup,fields=('__all__'),extra=7)
    helper = WCGroupForm.helper
    if request.method == 'POST':
        formset = WCGroupFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = WCGroupFormset(queryset=WCGroup.objects.none())
    else:
        formset = WCGroupFormset(queryset=WCGroup.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

def RoutingCreate(request):
    RoutingFormset = modelformset_factory(Routing,fields=('__all__'),extra=7,widgets={'code':autocomplete.ModelSelect2(url='material-autocomplete')})
    helper = RoutingForm.helper
    if request.method == 'POST':
        formset = RoutingFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = RoutingFormset(queryset=Routing.objects.none())
    else:
        formset = RoutingFormset(queryset=Routing.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)

@permission_required("app1.change_so",login_url='/accounts/login/')  
def SoUpdate(request):
    fields=('so','code','so_date','so_del_date','so_qty','closed','remarks')
    SoUpFormset = modelformset_factory(So,fields=fields,widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete',attrs={'width':'200px'})},can_delete=True)
    helper = SoForm1.helper
    f = SoFilter(request.GET, queryset=So.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = SoUpFormset(request.POST)
        #for form in formset:
        #    if form.is_valid() and form.has_changed():
        if formset.is_valid():
            formset.save()
        if not formset.is_valid():
            print(formset.errors)
            messages.error(request, "Please correct the errors below and resubmit.")
        else:
            formset = SoUpFormset(queryset=page_query)
    else:
        formset = SoUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)


@permission_required("app1.change_dispatch",login_url='/accounts/login/')  
def DispatchUpdate(request):
    DispatchUpFormset = modelformset_factory(Dispatch,fields=('__all__'))
    helper = DispatchForm.helper
    f = DispatchFilter(request.GET, queryset=Dispatch.objects.all())
    paginator = Paginator(f.qs, 25)
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

@permission_required("app1.change_line",login_url='/accounts/login/')  
def LineUpdate(request):
    LineUpFormset = modelformset_factory(Line,fields=('__all__'))
    helper = LineForm.helper
    f = LineFilter(request.GET, queryset=Line.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = LineUpFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = LineUpFormset(queryset=page_query)
    else:
        formset = LineUpFormset(queryset=page_query)
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

@permission_required("app1.change_material",login_url='/accounts/login/')  
def MaterialUpdate(request):
    MaterialUpFormset = modelformset_factory(Material,exclude=('des_code','cbm'),extra=0)
    helper = MaterialForm.helper
    f = MaterialFilter(request.GET, queryset=Material.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = MaterialUpFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            formset = MaterialUpFormset(queryset=page_query)
    else:
        formset = MaterialUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)

@permission_required("app1.change_bom",login_url='/accounts/login/')  
def BOMUpdate(request):
    BOMUpFormset = modelformset_factory(BOM,exclude=('des_code','cbm'),widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete'),'ccode':autocomplete.ModelSelect2(url='material-autocomplete')})
    helper = BOMForm.helper
    f = BOMFilter(request.GET, queryset=BOM.objects.all())
    paginator = Paginator(f.qs, 25,)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    query = f.qs
    page_query = query.filter(id__in=[object.id for object in page_obj])
    if request.method == 'POST':
        formset = BOMUpFormset(request.POST)
        if formset.has_changed() and formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            messages.error(request, "Please correct the errors below and resubmit.")
            formset = BOMUpFormset(queryset=page_query)
    else:
        formset = BOMUpFormset(queryset=page_query)
    context = {'formset': formset,'helper':helper,'filter': f,'page_obj': page_obj}
    return render(request,'app1/update_form.html',context)

class SoDetail1(UpdateView):
    model = So
    #form_class = SoForm
    template_name = 'app1/formmixin.html'
    fields=('id','so','so_date','so_del_date','closed','fgcode','customer','so_qty','act_disp_qty','act_disp_date')
    def get_success_url(self):
        return reverse_lazy('openso')
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
    #def post(self, request, pk):
    #    if 'confirm_delete' in self.request.POST:
     #       return self.delete(request)
    #def form_valid(self, form, pk):
    #    if 'confirm_post' in self.request.POST:
    #        form.instance.user = self.request.user
    #    return super(DispatchDetail, self).form_valid(form)

        
def BOMDetail(request,code_id=None):
    #model = BOM
    bomformset=modelformset_factory(BOM,fields=('__all__'),can_delete=True,extra=0,
                widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete'),'ccode':autocomplete.ModelSelect2(url='material-autocomplete')})
    template_name = 'app1/update_form.html'
    fields='__all__'
    helper = BOMForm.helper
    if request.method == 'POST':
        formset = bomformset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            print(formset.errors)
            formset = bomformset(queryset=BOM.objects.filter(code_id=code_id))
    else:
        formset = bomformset(queryset=BOM.objects.filter(code_id=code_id))
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/update_form.html',context)

class SoDetail(UpdateView):
    model = So
    template_name = 'app1/form.html'
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('openso')
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

class MaterialDetail(UpdateView):
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

class LineDetail(UpdateView):
    model = Line
    template_name = 'app1/form.html'
    fields='__all__'

class WCGroupDetail(UpdateView):
    model = WCGroup
    template_name = 'app1/form.html'
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('wcgrouplist')
        
class RoutingDetail(UpdateView):
    model = Routing
    template_name = 'app1/form.html'
    fields='__all__'
    def get_success_url(self):
        return reverse_lazy('routinglist')

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

class LineList(SingleTableMixin,FilterView):
    model = Line
    table_class = LineTable
    template_name = 'app1/list.html'
    filterset_class = LineFilter

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

class WCGroupList(SingleTableMixin,ExportMixin,FilterView):
    model = WCGroup
    template_name = 'app1/list.html'
    table_class = WCGroupTable
    #filterset_class = DispatchFilter

class RoutingList(SingleTableMixin,ExportMixin,FilterView):
    model = Routing
    template_name = 'app1/list.html'
    table_class = RoutingTable
    filterset_class = RoutingFilter

class ForecastList(SingleTableMixin,ExportMixin,FilterView):
    model = Forecast
    template_name = 'app1/list.html'
    table_class = ForecastTable
    #filterset_class = RoutingFilter

def visualization(request):
    pp = Plan.objects.values()
    df = pd.DataFrame(pp)
    ss = So.objects.values('id','so','so_del_date','code','so_qty','closed')
    df1 = pd.DataFrame(ss)
    df1 = df1.loc[df1.closed==0]
    df = pd.merge(df1,df,how='left',left_on='id',right_on='so_id')
    df = df[df.date.notnull()]
    sp = Speed.objects.values()
    df2 = pd.DataFrame(sp)
    df = pd.merge(df,df2,how='left',left_on=['code','line_id'],right_on=['code_id','line_id'])
    pr = Material.objects.values('code','case_size')
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
    print(df.info())
    pr = Material.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code_id'],right_on=['id'])
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

def matreqpivot(request):
    ss = So.objects.values()
    df = pd.DataFrame(ss)
    bm = BOM.objects.values()
    df1 = pd.DataFrame(bm)
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
    pr = Material.objects.values()
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
    pr = Material.objects.values()
    df3 = pd.DataFrame(pr)
    df = pd.merge(df,df3,how='left',left_on=['code_id'],right_on=['code'])
    df = df.to_html(table_id="input",index=False)
    context = {'df': df}
    return render(request, "app1/pivot.html", context)

def sodview(request):
    qs = So.objects.all()
    ff=[f.name for f in So._meta.get_fields()]
    ff.extend(['fgcode__'+k.name for k in Material._meta.get_fields()])
    ff.remove('fgcode__so')
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    d = dtale.show(df,name='so')
    try:
        response = redirect(d._main_url)
    except:
        response = redirect('http://asus:40000/dtale/main/so')
    return response

from django.db.models.expressions import RawSQL
def matreq(request):
    #qs = Material.objects.all()
    '''
    rqs = Material.objects.raw("SELECT m.id,m.code,m.desc, f.code AS fgcode,f.desc AS fdesc, SUM(s.so_qty) AS so_qty,b.qty as bqty, SUM(b.qty*s.so_qty) AS req FROM ((( app1_material m  
                                                                                              LEFT JOIN app1_bom b ON b.material_code_id=m.id)
                                                                                              LEFT JOIN app1_so s ON b.fgcode_id=s.fgcode_id)
                                                                                              LEFT JOIN app1_product f ON f.id=b.fgcode_id) WHERE s.closed=FALSE AND b.active=TRUE GROUP BY m.id,f.code,f.desc,bqty")
    
    sql=("SELECT DISTINCT m.code,m.desc FROM app1_bom b
            LEFT JOIN app1_material m ON (b.material_code_id = m.id)
            LEFT JOIN app1_product f ON (b.fgcode_id=f.id)
            LEFT JOIN app1_so s ON (s.fgcode_id = f.id)
            WHERE s.closed=FALSE AND b.active=TRUE GROUP BY m.code,m.desc")
    '''
    qs = BOM.objects.order_by().values('ccode').distinct().filter(code__so__closed=False).values('code_id','ccode__code','ccode__desc','code__code','code__desc','code__so__so','qty',
    'uom').annotate(bal_so_qty=F('code__so__so_qty')-Coalesce(Sum(F('code__so__dispatch__dis_qty')),0),req=F('qty')*F('bal_so_qty'))
    #print(qs)
    #qs = Material.objects.filter(pk__in=[x.pk for x in rqs])
    f = BOMFilter(request.GET, queryset=qs)
    paginate_by = 25
    table = MatreqTable(f.qs)
    RequestConfig(request, paginate={'per_page': 25, 'page': 1}).configure(table)
    return render(request, "app1/list.html", {"table": table,"filter":f})
    
def openso(request):
    qs= So.objects.filter(closed=False).annotate(production_sum=Sum('production__prod_qty')
    ,dispatch_sum=Subquery(Dispatch.objects.filter(so=OuterRef('pk')).values('so').annotate(the_sum=Sum('dis_qty'),).values('the_sum')[:1]))
    f = SoFilter(request.GET, queryset=qs)
    paginate_by = 25
    table = SoTable1(f.qs)
    RequestConfig(request, paginate={'per_page': 25, 'page': 1}).configure(table)
    return render(request, "app1/list.html", {"table": table,"filter":f})
    
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc
from django_plotly_dash import DjangoDash

def session_state_view(request, template_name, **kwargs):
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = DjangoDash('DjangoSessionState',add_bootstrap_links=True,external_stylesheets=external_stylesheets)
    qs = So.objects.all()
    ff=[f.name for f in So._meta.get_fields()]
    ff.extend(['code__'+k.name for k in Material._meta.get_fields()])
    ff.extend(['code__routing__wcgrp__wcgrp','code__routing__wcgrp__cap'])
    for i in ['code__so','code__id','act_disp_date','commit_disp_date','currency','act_disp_qty','rate','production','dispatch','plan','code',
            'code__des_code','code__customer','code__bom_ccode','code__stock','code__routing','code__rate','code__uom','code__lead_time','code__classification','code__cust_code','code__cbm','remarks','code__gr_wt','code__speed','code__bom']:
        ff.remove(i)
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df['so_del_date']=pd.to_datetime(df['so_del_date'],format='%Y-%m-%d')
    df['so_date']=pd.to_datetime(df['so_date'],format='%Y-%m-%d')
    df.rename(columns={'code__routing__wcgrp__wcgrp':'wc','code__routing__wcgrp__cap':'cap'},inplace=True)
    df['shift']=df['so_qty']*df['code__case_size']/df['cap']/8/0.68
    app.layout = html.Div([dbc.Row([
            dbc.Col(dcc.Dropdown(
            id='frequency', options=[{'label':i,'value':i} for i in ['D','W','M']],value='M')),
            dbc.Col(dcc.Dropdown(
            id='date',options=[{'label':i,'value':i} for i in ['so_date','so_del_date']], value='so_del_date')),
            dcc.DatePickerRange(id='daterange',start_date=df['so_date'].min(),end_date=df['so_del_date'].max(),calendar_orientation='vertical',persisted_props=[df['so_date'].min(),df['so_del_date'].max()])  
            ],className='mr-3 mt-3'),
        dcc.Graph(id='graph-with-slider'),
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns
            ],
            data=df.to_dict('records'),
            style_cell={'fontSize':17},
            locale_format={'so_date':'datetime'},
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            page_action="native",
            page_current= 0,
            page_size= 20,
    ),
    ])
    @app.callback(
         dash.dependencies.Output('graph-with-slider', 'figure'),
        [dash.dependencies.Input('frequency', 'value'),
         dash.dependencies.Input('date', 'value'),
         dash.dependencies.Input('daterange', 'start_date'),
         dash.dependencies.Input('daterange', 'end_date')]
        )
    def callback_color(freq_value,date,startdate,enddate):
        fdf=df[df[date]>startdate]
        fdf=fdf[fdf[date]<enddate]
        fdf.set_index(date,inplace=True)
        fdf=fdf.groupby([pd.Grouper(freq=freq_value),'wc']).agg('sum')
        fdf.reset_index(inplace=True)
        fdf.set_index(date,inplace=True)
        fig = px.bar(fdf,y="shift",facet_row="wc",height=900)
        for annotation in fig['layout']['annotations']: 
            annotation['textangle']= 0
        fig.update_yaxes(matches=None)
        fig.update_layout(transition_duration=500)
        return fig
    
    @app.callback(
        dash.dependencies.Output('datatable-interactivity','data'),
        [dash.dependencies.Input('graph-with-slider', 'clickData'),
          dash.dependencies.Input('date', 'value'),
          dash.dependencies.Input('frequency', 'value')]
        )
    def on_trace_click(click_data,date,freq):
        """Listen to click events and update table, passing filtered rows"""
        p = click_data['points'][0]
        key=pd.to_datetime(0)
        if 'x' in p:
            key = pd.to_datetime(p['x'])
        df_f = get_corresponding_rows(df, key,date,freq)
        return df_f.to_dict('records')

    def get_corresponding_rows(df, my_key,date,freq):
        """Filter df, return rows that match my_key"""
        ret = pd.DataFrame()
        if freq=='M':
            ret = df.loc[(df[date].dt.month == my_key.month) & (df[date].dt.year == my_key.year)]
        elif freq=='W':
            ret= df.loc[(df[date].dt.week == my_key.week) & (df[date].dt.week == my_key.week)]
        else:
            ret= df.loc[df[date] == my_key]
        return ret
        
    return render(request, template_name=template_name,)
    
def forecast_view(request, template_name, **kwargs):
    import joblib
    import datetime
    from dateutil import relativedelta
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = DjangoDash('DjangoSessionState',add_bootstrap_links=True,external_stylesheets=external_stylesheets)
    qs = So.objects.all()
    fo = Forecast.objects.all()
    ff= ['so_del_date','so_qty','code__code','code__desc']
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df['so_del_date']=pd.to_datetime(df['so_del_date'])
    foc= ['dem_month','fore_qty','code__code','code__desc','month']
    df1 = read_frame(fo,fieldnames=foc,coerce_float=True,index_col='id')
    df1['dem_month']=pd.to_datetime(df1['dem_month'])
    df1['month']=pd.to_datetime(df1['month'])
    app.layout = html.Div([dbc.Row([
            dbc.Col(dcc.Dropdown(id='code',options=[{'label':i,'value':i} for i in df['code__code'].unique()], value='FB24910000CA')),
            dbc.Col(dcc.Dropdown(id='month',options=[{'label':i,'value':i} for i in df1['month'].dt.date.unique()], value='')),
            dcc.DatePickerRange(id='daterange',start_date=df['so_del_date'].min(),end_date=datetime.date.today()+relativedelta.relativedelta(months=+5),calendar_orientation='vertical',persisted_props=[df['so_del_date'].min(),df['so_del_date'].max()])  
            ],className='mr-3 mt-3'),
        dcc.Graph(id='graph-with-slider'),
    ])
    @app.callback(
         dash.dependencies.Output('graph-with-slider', 'figure'),
        [dash.dependencies.Input('code', 'value'),
         dash.dependencies.Input('month', 'value'),
         dash.dependencies.Input('daterange', 'start_date'),
         dash.dependencies.Input('daterange', 'end_date')]
        )
    def callback_color(code,month,startdate,enddate):
        df2=df.set_index('so_del_date')
        df2=df2.groupby(['code__code','code__desc']).resample('M').sum()
        df2.rename(columns={'so_qty':'qty'},inplace=True)
        df2['type']="Actual"
        df3=df1[df1['month']==month]
        df3=df3.set_index('dem_month')
        df3=df3.groupby(['code__code','code__desc']).resample('M').sum()
        df3.rename(columns={'fore_qty':'qty'},inplace=True)
        df3['type']="Forecast"
        df2=df2.append(df3)
        df2.reset_index(inplace=True)
        fdf=df2[df2['so_del_date']>startdate]
        fdf=fdf[fdf['so_del_date']<enddate]
        fdf=fdf[fdf['code__code']==code]
        # Calculate prediction interval
        #sum_errs = arraysum((y - yhat)**2)
        #stdev = sqrt(1/(len(y)-2) * sum_errs)
        #interval = 1.96 * stdev
        #lower, upper = yhat_out - interval, yhat_out + interval
        
        fig = px.line(fdf,y="qty",x='so_del_date',height=500,color='type')
        fig.update_layout(transition_duration=500)
        return fig
        
    return render(request, template_name=template_name,)    
    
def forecast(request):
    import datetime
    from dateutil import relativedelta
    qs= So.objects.all()
    ff= ['so','so_del_date','so_qty','code__id','rate','code__code']
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df['so_del_date']=pd.to_datetime(df['so_del_date'])
    df['days'] = (df['so_del_date'] - df['so_del_date'].min()).dt.days
    df1=df.drop('code__code',axis=1)
    df1=df.set_index('so_del_date')
    df1=df1.groupby(['code__id','rate']).resample('M').sum()[['so_qty']]
    df1=df1.reset_index()
    df1['year']=df1.so_del_date.dt.year
    df1['month']=df1.so_del_date.dt.month
    df1['days'] = (df1['so_del_date'] - df1['so_del_date'].min()).dt.days
    df3=df1[df1['so_del_date'].dt.date<datetime.date.today()+relativedelta.relativedelta(months=+1)]
    df5 = df3
    df5['train']='train'
    for i in df3['code__id'].unique():
        rate= df3[df3['code__id']==i].sort_values('days',ascending=False)['rate'].head(1).values[0]
        tdf=pd.DataFrame()
        for m in range(0,4):
            month = (datetime.date.today()+relativedelta.relativedelta(months=+m+1)).month
            year = (datetime.date.today()+relativedelta.relativedelta(months=+m+1)).year
            days = (datetime.date.today()+relativedelta.relativedelta(months=+m+1)-df3['so_del_date'].min().date()).days
            tdf=tdf.append({'code__id':i,'rate':rate,'year':year,'month':month,'days':days,'train':'test'},ignore_index=True)
        df5=df5.append(tdf)
    df5['month'] = df5['month'].astype('category')
    df5['year'] = df5['year'].astype('category')
    df5['code__id']=df5['code__id'].astype('int')
    from .script import genmodel,genforecast
    if request.method == 'POST' and 'model_script' in request.POST:
        genmodel(df5)
    if request.method == 'POST' and 'forecast_script' in request.POST:
        genforecast(df5)
        
    return render(request, "app1/forecast.html",{"df": df})