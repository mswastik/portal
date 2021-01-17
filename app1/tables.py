import django_tables2 as tables
from .models import *
from .choice import *
from .forms import DateInput
from django_select2.forms import Select2Widget,ModelSelect2Widget
import django_filters
from django.db import models
from django_tables2.utils import A 
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from dal import autocomplete

class SoWidget(ModelSelect2Widget):
    model = So
    search_fields = [
        'so__icontains',
        'fgcode__code__icontains',
        'fgcode__desc__icontains',
    ]
    
class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) for row in table.data)

class SoFilter(django_filters.FilterSet):
    del__gt = django_filters.DateFilter(field_name='so_del_date', lookup_expr='gte',widget=DateInput())
    del__lt = django_filters.DateFilter(field_name='so_del_date', lookup_expr='lte',widget=DateInput())
    customer__customer = django_filters.CharFilter(lookup_expr='icontains')
    so = django_filters.TypedMultipleChoiceFilter(choices=zip(So.objects.distinct().values_list('so',flat=True),So.objects.distinct().values_list('so',flat=True)),coerce=str,widget=autocomplete.Select2Multiple())
    #print(zip(So.objects.values_list('so',flat=True),So.objects.values_list('so',flat=True)))
    fgcode__code = django_filters.CharFilter(lookup_expr='icontains')
    fgcode__desc = django_filters.CharFilter(lookup_expr='icontains')
    fgcode__bus_category = django_filters.ChoiceFilter(choices=bus_cat_choices)
    fgcode__plant = django_filters.ChoiceFilter(choices=plant_choices)
    fgcode__prod_category = django_filters.ChoiceFilter(choices=category_choices)
    so_qty = django_filters.RangeFilter()
    class Meta:
        model = So
        fields = [ 'so_date', 'closed']

class DispatchFilter(django_filters.FilterSet):
    disp_date__gt = django_filters.DateFilter(field_name='dispatch_date', lookup_expr='gte',widget=DateInput())
    disp_date__lt = django_filters.DateFilter(field_name='dispatch_date', lookup_expr='lte',widget=DateInput())
    #qty = django_filters.RangeFilter()
    dis_qty = django_filters.LookupChoiceFilter(lookup_choices=[
        ('exact', 'Equals'),
        ('gt', 'Greater than'),
        ('lt', 'Less than'),
    ])
    so__so = django_filters.TypedMultipleChoiceFilter(choices=zip(So.objects.distinct().values_list('so',flat=True),So.objects.distinct().values_list('so',flat=True)),coerce=str,widget=autocomplete.Select2Multiple())
    so__fgcode__code = django_filters.CharFilter(lookup_expr='icontains')
    so__fgcode__bus_category = django_filters.ChoiceFilter(choices=bus_cat_choices)
    so__fgcode__prod_category = django_filters.ChoiceFilter(choices=category_choices)
    class Meta:
        model = Dispatch
        exclude= ('so')
        
class ProductionFilter(django_filters.FilterSet):
    prod_date_gt = django_filters.DateFilter(field_name='prod_date', lookup_expr='gte',widget=DateInput())
    prod_date_lt = django_filters.DateFilter(field_name='prod_date', lookup_expr='lte',widget=DateInput())
    #customer = django_filters.CharFilter(lookup_expr='icontains')
    so__so = django_filters.CharFilter(lookup_expr='icontains')
    so__fgcode__code = django_filters.CharFilter(lookup_expr='icontains')
    prod_qty = django_filters.RangeFilter()
    #code__desc = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Production
        exclude= ('so','id','prod_date')
    

class PlanFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date',widget=DateInput())
    so__code = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Plan
        exclude = ()
        
class BOMFilter(django_filters.FilterSet):
    material_code__desc = django_filters.CharFilter(lookup_expr='icontains')
    fgcode__code = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = BOM
        exclude = ('material_code','fgcode')
    

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        exclude = ()

class MaterialFilter(django_filters.FilterSet):
    desc = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    lead_time = django_filters.RangeFilter()
    class Meta:
        model = Material
        exclude = ()

class SoTable(tables.Table):
    class Meta:
        model = So
        #fields = ('so','so_date','so_del_date','qty','fgcode')
        exclude = ('currency','remarks','rate','id','act_disp_date')
        attrs = {'class': 'table table-sm'}
    so = tables.Column(linkify={"viewname":"sodetail", "args":[A("pk")]})
    fgcode = tables.Column(footer="Total of all pages:")
    so_qty = SummingColumn()
    #fgcode = tables.Column()
    #code = tables.Column(linkify={"viewname":"plandetail", "args":[A("so")]})
    #line = tables.Column(accessor='plan.line')
    #def render_roles(self):
        #code= self.context["so"].code
        #qty= self.context["so"].qty
        #line= self.context["Plan"].line
    #so = tables.RelatedLinkColumn()
    #qty = tables.Column(accessor='so.qty')
    
class SoTable1(tables.Table):
    so = tables.Column(linkify={"viewname":"sodetail", "args":[A("pk")]})
    fgcode = tables.Column(footer="Total of all pages:")
    so_qty = SummingColumn()
    production_sum = tables.Column()
    dispatch_sum = tables.Column()
    class Meta:
        model = So
        fields = ('so','so_date','so_del_date','fgcode','so_qty','production_sum','prod_balance','dispatch_sum')
        #exclude = ('currency','remarks','rate','id','act_disp_date')
        attrs = {'class': 'table table-sm'}
    #def render_balance(self, value, record):
        #return format_html("{}-{}", record.qty, record.production_sum)
    #balance = tables.Column()
    #balance = tables.Column(accessor=("{{record.qty}}-{{record.production_sum}}"))
    def render_prod_balance(self, value, column):
        if value <= 5:
            column.attrs = {'td': {'bgcolor': 'lightgreen'}}
        else:
            column.attrs = {'td': {}}
        return value
    
class ProductTable(tables.Table):
    class Meta:
        model = Product
        #fields = ('code','desc','case_size','bulk_code','micro','carton')
        exclude = ()
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"productdetail", "args":[A("pk")]})
    
class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        exclude = ()
        attrs = {'class': 'table table-sm'}
    customer = tables.Column(linkify={"viewname":"productdetail", "args":[A("pk")]})
    
class MaterialTable(tables.Table):
    class Meta:
        model = Material
        exclude = ('id',)
        #fields = ('code','desc','fgcode','fdesc','uom','so_qty','bqty','req')
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"materialdetail", "args":[A("pk")]})


class MaterialTable1(tables.Table):
    class Meta:
        model = Material
        #exclude = ('id',)
        fields = ('code','desc','fgcode','fdesc','uom','so_qty','bqty','req')
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"materialdetail", "args":[A("pk")]})
    #used_in = tables.Column(linkify=True)
    #bom = tables.ManyToManyColumn(linkify_item=True,separator="",transform=lambda obj: format_html('{}<br/>'.format(obj)))
    #fgcode = tables.ManyToManyColumn(linkify_item=True)
    so_qty = tables.Column()
    req = tables.Column()
    #code__material_code__bomversion = tables.ManyToManyColumn(accessor='bom.bomversion',linkify_item=True)
    #def render_bom(self,value):
    #    return mark_safe(value)

class BOMTable(tables.Table):
    class Meta:
        model = BOM
        #fields = ('bomversion','material_code__material_id','qty')
        exclude = ('id',)
        attrs = {'class': 'table table-sm'}
    fgcode = tables.Column(linkify={"viewname":"bomdetail", "args":[A("fgcode_id")]})
    material_code = tables.Column(linkify=True)
    #material_code__material_id = tables.Column()

class DispatchTable(tables.Table):
    class Meta:
        model = Dispatch
        #fields = ('code','desc','case_size','bulk_code','micro','carton')
        exclude = ()
        attrs = {'class': 'table table-sm'}
    so = tables.Column(linkify={"viewname":"dispatchdetail", "args":[A("pk")]})
    dis_qty = SummingColumn()
        
class ProductionTable(tables.Table):
    class Meta:
        model = Production
        #fields = ('code','desc','case_size','bulk_code','micro','carton')
        exclude = ('id',)
        attrs = {'class': 'table table-sm'}
    so = tables.Column(linkify={"viewname":"productiondetail", "args":[A("pk")]})
    prod_qty = SummingColumn()

class PlanTable(tables.Table):
    class Meta:
        model = Plan
        fields = ('so','so_del_date','code','plan_qty','date')
        attrs = {'class': 'table table-sm'}
    so = tables.Column(linkify={"viewname":"sodetail", "args":[A("pk")]})
    #code = tables.Column()
    date = tables.Column()
    line = tables.Column(accessor='plan.line')
    #def render_roles(self):
        #code= self.context["so"].code
        #qty= self.context["so"].qty
        #so_del_date = self.context["so"].so_del_date
        #line= self.context["plan"].line
    #so = tables.RelatedLinkColumn()
    #qty = tables.Column(accessor='so.qty')
    def render_date(self, record):
        # phone is the name of the related manager
        if record.plan.exists():
            return str([p.pk for p in record.plan.all()])