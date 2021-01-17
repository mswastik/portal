import django_tables2 as tables
from .models import So,Product,Plan
from .forms import DateInput
import django_filters
from django import forms
from django.db import models
from django_tables2.utils import A 

class SoFilter(django_filters.FilterSet):
    del__lt = django_filters.DateFilter(field_name='so_del_date',widget=DateInput())
    del__gt = django_filters.DateFilter(field_name='so_del_date', lookup_expr='gt',widget=DateInput())
    customer = django_filters.CharFilter(lookup_expr='icontains')
    so = django_filters.CharFilter(lookup_expr='icontains')
    code__desc = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = So
        fields = [ 'so_date', 'closed']

class PlanFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name='date',widget=DateInput())
    so__code__desc = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = Plan
        exclude = ()


class SoTable(tables.Table):
    class Meta:
        model = So
        fields = ('so','so_date','so_del_date','qty')
    so = tables.Column(linkify={"viewname":"sodetail", "args":[A("pk")]})
    code = tables.Column()
    #code = tables.Column(linkify={"viewname":"plandetail", "args":[A("so")]})
    #line = tables.Column(accessor='plan.line')
    def render_roles(self):
        code= self.context["so"].code
        #qty= self.context["so"].qty
        #line= self.context["Plan"].line
    #so = tables.RelatedLinkColumn()
    #qty = tables.Column(accessor='so.qty')

class PlanTable(tables.Table):
    class Meta:
        model = Plan
        fields = ('so','so_del_date','code','qty','date')
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