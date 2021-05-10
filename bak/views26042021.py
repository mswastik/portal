from django.shortcuts import render,get_object_or_404
from .models import *
from .tables import *
from .forms import *
from .admin import SOResource
from django.forms import modelformset_factory,inlineformset_factory,formset_factory,CheckboxInput
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
#from .custom_layout_object import Formset
from django_pandas.io import read_frame
import dtale
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import messages
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin
from django import forms
#from django_select2.forms import Select2Widget,ModelSelect2Widget
from datetime import datetime
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum,Count
from django_tables2.config import RequestConfig
from django.db.models import F,Subquery, OuterRef
from dal import autocomplete
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models.functions import Coalesce
import plotly.io as pio
from funky_sheets.formsets import HotView

pio.templates.default = "plotly_white"
# Create your views here.
def index(request):
    model = So
    return render(request,'app1/base.html')

soinlineformset =  inlineformset_factory(So, Plan,form=PlanForm,widgets={'date': DateInput()},extra=5,can_delete=True)

'''    
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
'''
@permission_required("app1.add_so",login_url='/accounts/login/')   
def SoCreate(request):
    SoFormSet = modelformset_factory(So, fields=('so','code','so_date','so_del_date','closed','customer','so_qty','rate'), extra=12,
					widgets={'code': autocomplete.ModelSelect2(url='product-autocomplete'),'so_date': DateInput(),'so_del_date': DateInput()})
    helper = SoForm.helper
    #helper.field_class = 'input-group-sm form-control-sm mt-0'  #working

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
    DispatchFormset = modelformset_factory(Dispatch,fields=('__all__'),extra=12,widgets={'dispatch_date':DateInput,'so':autocomplete.ModelSelect2(url='openso-autocomplete')})
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
    BOMFormset = modelformset_factory(BOM,fields=('__all__'),extra=10,widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete'),'ccode':autocomplete.ModelSelect2(url='material-autocomplete')})
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
    MaterialFormset = modelformset_factory(Material,exclude=('cbm','pts','cust_code','des_code','lead_time'),extra=7,widgets={'material_code':autocomplete.ModelSelect2(url='material-autocomplete')})
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

def FmodelCreate(request):
    FmodelFormset = modelformset_factory(Fmodel,exclude=('smape','mae','mase'),extra=7,widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete')})
    helper = FmodelForm.helper
    if request.method == 'POST':
        formset = FmodelFormset(request.POST)
        for form in formset:
            if form.is_valid() and form.has_changed():
                form.save()
            else:
                formset = FmodelFormset(queryset=Fmodel.objects.none())
    else:
        formset = FmodelFormset(queryset=Fmodel.objects.none())
    context = {'formset': formset,'helper':helper}
    return render(request,'app1/create_form.html',context)


class CreateSoView(HotView):
    # Define model to be used by the view
    model = So
    # Define template
    template_name = 'app1/excel.html'
    # Define custom characters/strings for checked/unchecked checkboxes
    checkbox_checked = 'yes' # default: true
    checkbox_unchecked = 'no' # default: false
    # Define prefix for the formset which is constructed from Handsontable spreadsheet on submission
    prefix = 'table'
    # Define success URL
    success_url = reverse_lazy('soxupdate')
    # Define fields to be included as columns into the Handsontable spreadsheet
    fields = (
        'so',
        'so_date',
        'so_del_date',
        'code',
        'so_qty',
        'closed',
    )
    # Define extra formset factory kwargs
    factory_kwargs = {
        'widgets': {
            'so_date': DateInput(attrs={'type': 'date'}),
            'so_del_date': DateInput(attrs={'type': 'date'}),
            'closed': CheckboxInput(),
        }
    }
    # Define Handsontable settings as defined in Handsontable docs
    hot_settings = {
        'contextMenu': 'true',
        'autoWrapRow': 'true',
        'rowHeaders': 'true',
        'contextMenu': 'true',
        'search': 'true',
        'licenseKey': 'non-commercial-and-evaluation',
        # When value is dictionary don't wrap it in quotes
        'headerTooltips': {
            'rows': 'false',
            'columns': 'true'
        },
        # When value is list don't wrap it in quotes
        'dropdownMenu': [
            'remove_col',
            '---------',
            'make_read_only',
            '---------',
            'alignment'
        ]
    }

class UpdateSoView(CreateSoView):
  template_name = 'app1/excel.html'
  # Define 'update' action
  action = 'update'
  # Define 'update' button
  button_text = 'Update'
  def get_queryset(self):
        #code = self.kwargs['code_id']
        return self.model.objects.filter(code_id=10605)


@permission_required("app1.change_so",login_url='/accounts/login/')  
def SoUpdate(request):
    fields=('so','code','so_date','so_del_date','so_qty','closed','remarks')
    SoUpFormset = modelformset_factory(So,fields=fields,widgets={'code':autocomplete.ModelSelect2(url='product-autocomplete'),
                                        'so_date':DateInput,'so_del_date':DateInput},can_delete=True)
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
    DispatchUpFormset = modelformset_factory(Dispatch,fields=('__all__'),widgets={'so':autocomplete.ModelSelect2(url='openso-autocomplete')})
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
                plan.save()
        return super(SoDetail, self).form_valid(form)
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_tag = True
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
        form.helper.form_method = 'post'
        form.helper.add_input(Submit('submit', 'Update', css_class='btn-primary'))
        return form


class ProductionDetail(UpdateView):
    model = Production
    template_name = 'app1/form.html'
    form_class = ProductionForm1
    def get_success_url(self):
        return reverse_lazy('productionlist')

class DispatchDetail(UpdateView):
    model = Dispatch
    template_name = 'app1/form.html'
    form_class = DispatchForm1
    def get_success_url(self):
        return reverse_lazy('dispatchlist')
        
def BOMDetail(request,code_id=None):
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

def FmodelDetail(request,pk=None):
    qs = Fmodel.objects.filter(id=pk)
    import datetime
    from dateutil import relativedelta
    ff= ['id','model','alg','code__so__so_del_date','code__so__so_qty','code__so__rate']
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df = df.rename(columns={'code__so__so_del_date': 'so_del_date', 'code__so__rate': 'rate','code__so__so_qty': 'so_qty',})
    df['so_del_date']=pd.to_datetime(df['so_del_date'])
    df1=df.set_index('so_del_date').resample('M').agg({"so_qty":np.sum,"rate":np.mean}).copy()
    df1['rate']=df1['rate'].ffill()
    df1['month']=df1.index.month
    df1=df1[df1.index.date<datetime.date.today()+relativedelta.relativedelta(months=+1)]
    df1['month'] = df1['month'].astype('category')
    context ={}
    from .script import genforecast1,savemodel,exploremodel
    if request.method == 'POST' and 'savemodel' in request.POST:
        savemodel(df1,pk)
    if request.method == 'POST' and 'genforecast1' in request.POST:
        context=genforecast1(df1,pk)
    if request.method == 'POST' and 'expforecast1' in request.POST:
        context=exploremodel(df1,pk) 
    return render(request, "app1/forecast1.html",context)

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

class CustomerDetail(UpdateView):
    model = Customer
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
    template_name = 'app1/list.html'
    filterset_class = SoFilter

class CustomerList(SingleTableMixin,ExportMixin,FilterView):
    model = Customer
    paginate_by = 20
    table_class = CustomerTable
    template_name = 'app1/list.html'

class PlanList(SingleTableMixin,FilterView):
    model = Plan
    table_class = PlanTable
    template_name = 'app1/list.html'
    filterset_class = PlanFilter

class SpeedList(SingleTableMixin,FilterView):
    model = Speed
    template_name = 'app1/list.html'

class LineList(FormMixin,ListView):
    model = Line
    #table_class = LineTable
    template_name = 'app1/table_form.html'
    form_class = LineForm
    #filterset_class = LineFilter
    def post(self, request, *args, **kwargs):
        form = LineForm(request.POST)
        if form.is_valid():
            #sub = Subscriber(email=request.POST['email'], conf_num=random_digits())
            form.save()
            return render(request, "app1/table_form.html", {'form': LineForm()}) 
        else:
            return render(request, "app1/table_form.html", {'form': LineForm()}) 
    
class FmodelList(SingleTableMixin,FilterView):
    model = Fmodel
    table_class = FmodelTable
    template_name = 'app1/list.html'
    filterset_class = FmodelFilter

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
    filterset_class = ForecastFilter

class PlanningList(SingleTableMixin,ExportMixin,FilterView):
    model = Planning
    template_name = 'app1/list.html'

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

def fmodelpivot(request):
    ss = Fmodel.objects.all()
    ff=[f.name for f in Fmodel._meta.get_fields()]
    ff.extend(['code__code','code__desc'])
    df = read_frame(ss,fieldnames=ff,coerce_float=True,index_col='id')
    #df = pd.DataFrame(ss)
    #print(df.info())
    #pr = Material.objects.values()
    #df3 = pd.DataFrame(pr)
    #df = pd.merge(df,df3,how='left',left_on=['code_id'],right_on=['id'])
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
    #ff.extend(['code__'+k.name for k in Material._meta.get_fields()]) #Get field names of related models also
    ff.extend(['code__'+k.name for k in Material._meta.fields])
    tt=['production','dispatch','plan','commit_disp_date','act_disp_qty','currency','code__rate','code__uom','code__customer','code__cbm','code__lead_time','code__des_code','code__cust_code']
    ff=[ele for ele in ff if ele not in tt]
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df['so_del_date'] = pd.to_datetime(df['so_del_date'])
    df['so_date'] = pd.to_datetime(df['so_date'])
    d = dtale.show(df,name='so')
    try:
        response = redirect(d._main_url)
    except:
        response = redirect('http://asus:40000/dtale/main/so')
    return response
    
def forecastdview(request):
    qs = So.objects.all()
    #ff=[f.name for f in So._meta.get_fields()]
    #ff.extend(['code__'+k.name for k in Material._meta.get_fields()]) #Get field names of related models also
    #ff.extend(['code__forecast__dem_month','code__forecast__fore_qty__avg'])
    #tt=['production','dispatch','plan','commit_disp_date','act_disp_qty','currency','code__rate','code__uom','code__customer','code__cbm','code__lead_time','code__des_code','code__cust_code']
    #ff=[ele for ele in ff if ele not in tt]
    ff=['id','so_del_date','code_id__code','code_id__desc','so_qty']
    df = read_frame(qs,fieldnames=ff,coerce_float=True,index_col='id')
    df['so_del_date'] = pd.to_datetime(df['so_del_date'])
    df['type'] = 'SO'
    qs1 = Forecast.objects.all().filter(version=1)
    kk=['id','dem_month','code_id__code','code_id__desc','fore_qty']
    df1 = read_frame(qs1,fieldnames=kk,coerce_float=True,index_col='id')
    df1['dem_month'] = pd.to_datetime(df1['dem_month'])
    df1['type'] = 'Forecast'
    df.rename(columns={'so_del_date':'dem_month','so_qty':'fore_qty'},inplace=True)
    df=df.append(df1,ignore_index=True)
    d = dtale.show(df,name='forecast')
    try:
        response = redirect(d._main_url)
    except:
        response = redirect('http://asus:40000/dtale/main/forecast')
    return response

from django.db.models.expressions import RawSQL
def matreq(request):
    qs = BOM.objects.order_by().values('ccode').distinct().filter(code__so__closed=False).values('code_id','ccode__code','ccode__desc','code__code','code__desc','code__so__so','qty',
    'uom').annotate(bal_so_qty=F('code__so__so_qty')-Coalesce(Sum(F('code__so__dispatch__dis_qty')),0),req=F('qty')*F('bal_so_qty'))
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
 
import datetime
from dateutil import relativedelta 
def forecast_view(request, template_name, **kwargs):
    #external_stylesheets = ['D:\\SwastikMishra\\Downloads\\data\\mysite1\\app1\\static\\bWLwgP.css']
    app = DjangoDash('DjangoSessionState',add_bootstrap_links=True)
    #app.css.config.serve_locally = True
    #app.scripts.config.serve_locally = True
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
    df1=df.groupby(['code__id',pd.Grouper(freq='M',key='so_del_date')]).agg({"so_qty":np.sum,"rate":np.mean}).copy()
    df1['rate']=df1['rate'].ffill()
    df1=df1.reset_index()
    df1.set_index('so_del_date',inplace=True)
    df1=df1[df1.index.date<datetime.date.today()+relativedelta.relativedelta(months=+1)]
    from .script import genmodel,genforecast,genmps
    if request.method == 'POST' and 'model_script' in request.POST:
        genmodel(df1)
    if request.method == 'POST' and 'forecast_script' in request.POST:
        genforecast(df1)
    if request.method == 'POST' and 'mps_script' in request.POST:
        df=genmps(df1)
    return render(request, "app1/forecast.html",{"df": df})

from pandas.tseries.offsets import MonthBegin    
from django.forms import inlineformset_factory
from django.db.models import Case, Value, When

def html_input(c):
    return '<input name="{}" value="{{}}" />'.format(c)

def mps(request):
    form=MaterialUnique()
    forecastFormset=modelformset_factory(Forecast, fields=('id','code','dem_month','fore_qty','overr_qty'),extra=0)
    #query= Forecast.objects.values('code__code').distinct()
    formset1 = forecastFormset(queryset=Forecast.objects.none())
    #mpsFormset=modelformset_factory(Planning, fields=('id','code','month','mps_qty'),widgets={'month':DateInput},extra=12)
    #formset = mpsFormset(queryset=Planning.objects.none())
    context={}
    uni=''
    df1=""
    if request.method == 'POST' and 'code' in request.POST:
        form=MaterialUnique(request.POST)
        #uni = form.cleaned_data['code']
        uni = request.POST.getlist('code')[0]
        #formset = mpsFormset(queryset=Planning.objects.filter(code_id__code=form))
        query=Forecast.objects.filter(code_id__code=uni,month=pd.to_datetime(datetime.date.today()- MonthBegin(n=1))).order_by('dem_month','version')
        #formset1 = forecastFormset(queryset=query)
        #formset1 = forecastFormset(request.POST)
        #context={'formset1':formset1,'form':form}
        ff=['id','code__id','code__code','fore_qty','overr_qty','dem_month']
        df = read_frame(query,fieldnames=ff,coerce_float=True,index_col='id')
        df['SO']=''
        df['PAB']=''
        df['MPS']=''
        #df=df.melt(['code__id','dem_month','code__code']).pivot(['code__id','code__code','variable'],'dem_month')
        df1=df.style.format({c: html_input(c) for c in df.columns}).render()
    if request.method == 'POST' and 'forecast' in request.POST:
        formset1 = forecastFormset(request.POST)
        #print(formset1)
        if formset1.is_valid():
            #print('valid form')
            formset1.save()
            #formset1 = forecastFormset(queryset=Forecast.objects.filter(code_id__code=form))
        else:
            print(formset1.errors)
            #formset1 = forecastFormset(queryset=Forecast.objects.filter(code_id__code=form))
    if request.method == 'POST' and 'df' in request.POST:
        #df = pd.DataFrame(request.POST.lists()[1],columns=request.POST.lists()[0])
        kk=dict(request.POST)# no .dict-keys 1 item, .items-0 values, .values-0 values 
        del kk['df']
        del kk['csrfmiddlewaretoken']
        #kk=kk.pop('csrfmiddlewaretoken')
        df=pd.DataFrame(kk)
        print(df)
        #for i in range(len(df)):
        #    Forecast.objects.update(fore_qty=Case(When(code_id=df['code__id'][0], month=pd.to_datetime(datetime.date.today()- MonthBegin(n=1)),version=i+1, 
        #    dem_month=df['dem_month'][i], then=df['fore_qty'][i]),default=0))
        '''
        for form in formset1:
            if form.is_valid():
                form.save()
        
    if request.method == 'POST' and 'mps' in request.POST:
        formset = mpsFormset(request.POST)
        for form in formset:
            if form.has_changed() and form.is_valid():
                form.save()
                print(uni)
            else:
                print(uni)
                print(form.errors)
                formset = mpsFormset(queryset=Planning.objects.none())'''
    context={'formset1':formset1,'form':form,'df':df1}
    return render(request, "app1/plan.html",context)
 
from datatableview.views import DatatableView,XEditableDatatableView
from datatableview import helpers
class DatatableView(XEditableDatatableView):
    model = Forecast
    datatable_options = {
                'structure_template': "datatableview/bootstrap_structure.html",
                'columns': [
                ("forecast", 'Forecast', helpers.make_xeditable),
                ("overr_qty", 'Overr Qty', helpers.make_xeditable),
                ("dem_month", 'Dem Month', helpers.make_xeditable)],
                'search_fields': ['code'],
            }
            
from django.http import JsonResponse
def xed_post(request):
    """
    X-Editable: handle post request to change the value of an attribute of an object

    request.POST['model']: name of Django model of which an object will be changed
    request.POST['pk']: pk of object to be changed
    request.POST['name']: name of the field to be set
    request.POST['value']: new value to be set
    """
    try:
        if not 'name' in request.POST or not 'pk' in request.POST or not 'value' in request.POST:
            _data = {'success': False, 'error_msg': 'Error, missing POST parameter'}
            return JsonResponse(_data)

        _model = apps.get_model('swingit', request.POST['model'])  # Grab the Django model
        _obj = _model.objects.filter(pk=request.POST['pk']).first()  # Get the object to be changed
        setattr(_obj, request.POST['name'], request.POST['value'])  # Actually change the attribute to the new value
        _obj.save()  # And save to DB

        _data = {'success': True}
        return JsonResponse(_data)

    # Catch issues like object does not exist (wrong pk) or other
    except Exception as e:
        _data = {'success': False,
                'error_msg': f'Exception: {e}'}
        return JsonResponse(_data)