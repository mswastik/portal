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
from dal import forward

class SoWidget(ModelSelect2Widget):
    model = So
    search_fields = [
        'so__icontains',
        'fgcode__code__icontains',
        'fgcode__desc__icontains',
    ]
    
class SummingColumn(tables.Column):
    def render_footer(self, bound_column, table):
        return sum(bound_column.accessor.resolve(row) or 0 for row in table.data)

class SoFilter(django_filters.FilterSet):
    del__gt = django_filters.DateFilter(field_name='so_del_date', lookup_expr='gte',widget=DateInput())
    del__lt = django_filters.DateFilter(field_name='so_del_date', lookup_expr='lte',widget=DateInput())
    customer__customer = django_filters.CharFilter(lookup_expr='icontains')
    so = django_filters.CharFilter(lookup_expr='icontains')
    code__code = django_filters.CharFilter(lookup_expr='icontains')
    code__desc = django_filters.CharFilter(lookup_expr='icontains')
    code__bus_category = django_filters.ChoiceFilter(choices=bus_cat_choices)
    code__plant = django_filters.ChoiceFilter(choices=plant_choices)
    code__prod_category = django_filters.ChoiceFilter(choices=category_choices)
    so_qty = django_filters.RangeFilter()
    class Meta:
        model = So
        fields = [ 'so_date', 'closed']

class DispatchFilter(django_filters.FilterSet):
    disp_date__gt = django_filters.DateFilter(field_name='dispatch_date', lookup_expr='gte',widget=DateInput())
    disp_date__lt = django_filters.DateFilter(field_name='dispatch_date', lookup_expr='lte',widget=DateInput())
    dis_qty = django_filters.LookupChoiceFilter(lookup_choices=[
        ('exact', 'Equals'),
        ('gt', 'Greater than'),
        ('lt', 'Less than'),
    ])
    #so__so = django_filters.TypedMultipleChoiceFilter(choices=zip(So.objects.distinct().values_list('so',flat=True),So.objects.distinct().values_list('so',flat=True)),coerce=str,widget=autocomplete.Select2Multiple())
    so__so = django_filters.CharFilter(lookup_expr='icontains')
    so__code__code = django_filters.CharFilter(lookup_expr='icontains')
    so__code__desc = django_filters.CharFilter(lookup_expr='icontains')
    so__code__bus_category = django_filters.ChoiceFilter(choices=bus_cat_choices)
    so__code__prod_category = django_filters.ChoiceFilter(choices=category_choices)
    class Meta:
        model = Dispatch
        exclude= ('so')
        
class ProductionFilter(django_filters.FilterSet):
    prod_date_gt = django_filters.DateFilter(field_name='prod_date', lookup_expr='gte',widget=DateInput())
    prod_date_lt = django_filters.DateFilter(field_name='prod_date', lookup_expr='lte',widget=DateInput())
    #customer = django_filters.CharFilter(lookup_expr='icontains')
    so__so = django_filters.CharFilter(lookup_expr='icontains')
    so__code__code = django_filters.CharFilter(lookup_expr='icontains')
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

class LineFilter(django_filters.FilterSet):
    line = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Line
        exclude = ()

class FmodelFilter(django_filters.FilterSet):
    code__code = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Fmodel
        exclude = (['model','code'])
        
class BOMFilter(django_filters.FilterSet):
    ccode__code = django_filters.CharFilter(lookup_expr='icontains')
    ccode__desc = django_filters.CharFilter(lookup_expr='icontains')
    code__code = django_filters.CharFilter(lookup_expr='icontains')
    code__desc = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = BOM
        exclude = ('code','ccode',)
    
class ForecastFilter(django_filters.FilterSet):
    code__code = django_filters.CharFilter(lookup_expr='icontains')
    code__desc = django_filters.CharFilter(lookup_expr='icontains')
    month = django_filters.DateFilter(field_name='month', lookup_expr='gte',widget=DateInput())
    class Meta:
        model = Forecast
        exclude = ('id','code')

class MaterialFilter(django_filters.FilterSet):
    desc = django_filters.CharFilter(lookup_expr='icontains')
    code = django_filters.CharFilter(lookup_expr='icontains')
    lead_time = django_filters.RangeFilter()
    remarks = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Material
        exclude = ()

class RoutingFilter(django_filters.FilterSet):
    code = django_filters.CharFilter(widget=autocomplete.ListSelect2(url='material-autocomplete'))
    #lead_time = django_filters.RangeFilter()
    class Meta:
        model = Routing
        exclude = ()

class SoTable(tables.Table):
    class Meta:
        model = So
        #fields = ('so','so_date','so_del_date','qty','fgcode')
        exclude = ('currency','remarks','rate','id','act_disp_date')
        attrs = {'class': 'table table-sm'}
    so = tables.Column(linkify={"viewname":"sodetail", "args":[A("pk")]})
    code = tables.Column(footer="Total of all pages:")
    so_qty = SummingColumn()
    #def render_roles(self):
        #code= self.context["so"].code
        #qty= self.context["so"].qty
        #line= self.context["Plan"].line
    #so = tables.RelatedLinkColumn()
    #qty = tables.Column(accessor='so.qty')
    
class SoTable1(tables.Table):
    so = tables.Column(linkify={"viewname":"sodetail", "args":[A("pk")]})
    code = tables.Column(footer="Total of all pages:")
    so_qty = SummingColumn()
    production_sum = tables.Column()
    dispatch_sum = tables.Column()
    class Meta:
        model = So
        fields = ('so','so_date','so_del_date','code','so_qty','production_sum','dispatch_sum')
        #exclude = ('currency','remarks','rate','id','act_disp_date')
        attrs = {'class': 'table table-sm'}
        order_by=('so_del_date','so')
    #def render_balance(self, value, record):
        #return format_html("{}-{}", record.qty, record.production_sum)
    #balance = tables.Column(accessor=("{{record.qty}}-{{record.production_sum}}"))
    def render_prod_balance(self, value, column):
        if value <= 5:
            column.attrs = {'td': {'bgcolor': 'lightgreen'}}
        else:
            column.attrs = {'td': {}}
        return value
    
class CustomerTable(tables.Table):
    class Meta:
        model = Customer
        exclude = ()
        attrs = {'class': 'table table-sm'}
    customer = tables.Column(linkify={"viewname":"productdetail", "args":[A("pk")]})
    
class MaterialTable(tables.Table):
    class Meta:
        model = Material
        exclude = ()
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"materialdetail", "args":[A("pk")]})

class FmodelTable(tables.Table):
    class Meta:
        model = Fmodel
        exclude = (['model'])
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"fmodeldetail", "args":[A("pk")]})

class MaterialTable1(tables.Table):
    class Meta:
        model = Material
        #exclude = ('id',)
        fields = ('code','desc','fgcode','fdesc','uom','so_qty','bqty','req')
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"materialdetail", "args":[A("pk")]})
    so_qty = tables.Column()
    req = tables.Column()

class BOMTable(tables.Table):
    class Meta:
        model = BOM
        exclude = ('id','bom_version')
        attrs = {'class': 'table table-sm'}
    code = tables.Column(linkify={"viewname":"bomdetail", "args":[A("code_id")]})
    material_code = tables.Column(linkify=True)

class ForecastTable(tables.Table):
    class Meta:
        model = Forecast
        exclude = ('id',)
        attrs = {'class': 'table table-sm'}


class DecimalColumn(tables.Column):   
    def __init__(self, *args, **kwargs):
        super(DecimalColumn, self).__init__(*args, **kwargs)
    def render(self,value):
       ff = forms.DecimalField()
       return ff.widget.render(self.verbose_name,value)

class HiddenInputColumn(tables.Column):
    def __init__(self, *args, **kwargs):
        kwargs['attrs'] = {'th': {'style': 'display:none;'},
                           'td': {'style': 'display:none;'}}
        super(HiddenInputColumn, self).__init__(*args, **kwargs)

    def render(self, value):
        return mark_safe('<input type="hidden" name="{}" value="{}" />'.format(self.verbose_name, value))
       
class LineTable(tables.Table):
    class Meta:
        model = Line
        exclude = ('id',)
        attrs = {'class': 'table table-sm'}
    line = tables.Column(linkify={"viewname":"linedetail", "args":[A("pk")]})
    capacity = DecimalColumn(verbose_name='capacity',accessor='capacity')
    #capacity = SummingColumn()
    prod_category = tables.Column(footer="Total of all pages:")
    idx = HiddenInputColumn(verbose_name='id', accessor='pk')
    


class WCGroupTable(tables.Table):
    class Meta:
        model = WCGroup
        exclude = ('id',)
        attrs = {'class': 'table table-sm'}
    wcgrp = tables.Column(linkify={"viewname":"wcgrpdetail", "args":[A("pk")]})

class RoutingTable(tables.Table):
    class Meta:
        model = Routing
        attrs = {'class': 'table table-sm'}
    id = tables.Column(linkify={"viewname":"routingdetail", "args":[A("pk")]})

class MatreqTable(tables.Table):
    class Meta:
        model = BOM
        fields = ('ccode__code','ccode__desc','code__code','code__desc','code__so__so','qty','uom','bal_so_qty','req')
        attrs = {'class': 'table table-sm'}
    ccode__code = tables.Column()
    ccode__desc = tables.Column()
    code__code = tables.Column(linkify={"viewname":"bomdetail", "args":[A("code_id")]})
    code__desc = tables.Column(footer="Total of all pages:")
    qty = tables.Column()
    req = SummingColumn()

class DispatchTable(tables.Table):
    class Meta:
        model = Dispatch
        exclude = ()
        attrs = {'class': 'table table-sm'}
        order_by = '-dispatch_date'
    so = tables.Column(linkify={"viewname":"dispatchdetail", "args":[A("pk")]})
    dispatch_date=tables.Column(order_by=("dispatch_date",))
    dis_qty = SummingColumn()
        
class ProductionTable(tables.Table):
    class Meta:
        model = Production
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
    date = tables.Column()
    line = tables.Column(accessor='plan.line')
    def render_date(self, record):
        # phone is the name of the related manager
        if record.plan.exists():
            return str([p.pk for p in record.plan.all()])