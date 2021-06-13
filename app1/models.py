from django.db import models
#from annoying.fields import AutoOneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from datetime import datetime,timedelta    
from .choice import *

# Create your models here.
class Customer(models.Model):
    customer = models.CharField(max_length=35)
    country = models.CharField(max_length=35,choices=country_choices,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.customer

class Material(models.Model):
    code = models.CharField(max_length=15,unique=True)
    desc = models.CharField(max_length=45)
    rate = models.DecimalField(max_digits=9,decimal_places=3,null=True,blank=True)
    uom = models.CharField(max_length=3)
    lead_time = models.IntegerField(default=0,null=True,blank=True)
    classification = models.CharField(max_length=10,choices=material_choices,null=True,blank=True)
    case_size = models.IntegerField(blank=True,null=True)
    micro = models.BooleanField(blank=True,null=True)
    bus_category = models.CharField(max_length=15,choices=bus_cat_choices,blank=True,null=True)
    prod_category = models.CharField(max_length=25,choices=category_choices,blank=True,null=True)
    gr_wt = models.DecimalField(max_digits=9,decimal_places=4,blank=True,null=True)
    nt_wt = models.DecimalField(max_digits=9,decimal_places=4,blank=True,null=True)
    plant = models.CharField(max_length=4,choices=plant_choices,blank=True,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    des_code = models.CharField(max_length=15,blank=True,null=True)
    cust_code = models.CharField(max_length=15,blank=True,null=True)
    pts = models.DecimalField(max_digits=9,decimal_places=4,blank=True,null=True)
    cbm = models.DecimalField(max_digits=9,decimal_places=4,blank=True,null=True)
    remarks = models.CharField(max_length=15,blank=True,null=True)
    lot_size = models.IntegerField(default=0,null=True,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {}'.format(self.code,self.desc)
    def get_absolute_url(self):
        return "/app1/materialdetail/%i" % self.id
 
class So(models.Model):
    so = models.CharField(max_length=25,verbose_name="Sales Order")
    so_date = models.DateField()
    so_del_date = models.DateField()
    code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True)
    so_qty = models.DecimalField(default=0,max_digits=7,decimal_places=1)
    closed = models.BooleanField(verbose_name='Closed')
    commit_disp_date = models.DateField(null=True,blank=True)
    act_disp_qty = models.IntegerField(default=0,null=True,blank=True)
    act_disp_date = models.DateField(null=True,blank=True)
    rate = models.DecimalField(max_digits=7,decimal_places=2,blank=True,null=True)
    currency = models.CharField(max_length=3,choices=curr_choices,blank=True,null=True)
    customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True)
    remarks = models.CharField(max_length=45,blank=True,null=True)
    #prod_comp = models.BooleanField()
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {} - {}'.format(self.so,self.code,self.so_qty)
    def get_absolute_url(self):
        return "/app1/sodetail/%i" % self.id
    

class Calendar(models.Model):
    date = models.DateTimeField()
    working = models.BooleanField()
    def __str__(self):              # __unicode__ on Python 2
        return self.date


class BOM(models.Model):
    code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True,blank=True)
    bom_version = models.IntegerField()
    ccode = models.ForeignKey(Material,related_name='bom_ccode',on_delete=models.SET_NULL,null=True,verbose_name='component',to_field='id',blank=True)
    qty = models.DecimalField(max_digits=11,decimal_places=4)
    uom = models.CharField(max_length=3,choices=uom_choices,blank=True)
    bom_type = models.CharField(max_length=4,choices=bom_choices)
    active = models.BooleanField(verbose_name='active')
    def __str__(self):              # __unicode__ on Python 2
        return '{}'.format(self.bom_version)
    def get_absolute_url(self):
        return "/app1/bomdetail/%i" % self.id

class Stock(models.Model):
    material_code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True)
    qty_released = models.DecimalField(max_digits=9,decimal_places=2)
    qty_quality = models.DecimalField(max_digits=9,decimal_places=2)
    uom = models.CharField(max_length=3)
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.material_code

class Line(models.Model):
    line = models.CharField(max_length=4,unique=True)
    plant = models.CharField(max_length=4,choices=plant_choices)
    prod_category = models.CharField(max_length=25,choices=category_choices)
    capacity = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
    uom = models.CharField(max_length=3,null=True,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return self.line
        
class Production(models.Model):
    so = models.ForeignKey(So, on_delete=models.CASCADE)
    line = models.ForeignKey(Line,on_delete=models.SET_NULL,null=True)
    date = models.DateField(default=datetime.today()-timedelta(1))
    shift = models.CharField(max_length=1,choices=shift_choices)
    prod_qty = models.DecimalField(max_digits=7,decimal_places=2)
    #doc_date = models.DateField(auto_now=True)
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {}'.format(self.so,self.prod_qty)

class Dispatch(models.Model):
    so = models.ForeignKey(So, on_delete=models.CASCADE)
    dispatch_date = models.DateField(default=datetime.now)
    dis_qty = models.DecimalField(max_digits=7,decimal_places=2)
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {}'.format(self.so,self.dis_qty)

class Speed(models.Model):
    code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True,to_field='code')
    line = models.ForeignKey(Line,on_delete=models.SET_NULL,null=True,to_field='line')
    speed = models.FloatField()
    manpower = models.DecimalField(max_digits=7,decimal_places=4,null=True,blank=True)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.speed)

class WCGroup(models.Model):
    wcgrp = models.CharField(max_length=5)
    cap = models.DecimalField(max_digits=9,decimal_places=4,null=True,blank=True)
    set_time = models.DecimalField(max_digits=4,decimal_places=1,null=True,blank=True)
    #line = models.ForeignKey(Line,on_delete=models.SET_NULL,null=True,to_field='line')
    def __str__(self):              # __unicode__ on Python 2
        return str(self.wcgrp)
        
class Routing(models.Model):
    code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True)
    wcgrp = models.ForeignKey(WCGroup,on_delete=models.SET_NULL,null=True)
    def __str__(self):              # __unicode__ on Python 2
        return str(self.code)

class Plan(models.Model):
    so = models.ForeignKey(So,on_delete=models.CASCADE, null=True,to_field='id', related_name='plan')
    date = models.DateTimeField(null=True,blank=True)
    line = models.ForeignKey(Line,on_delete=models.SET_NULL,blank=True,null=True,to_field='line')
    plan_qty = models.DecimalField(max_digits=7,decimal_places=2)
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {} - {}'.format(self.so,self.date,self.line)
    def get_absolute_url(self):
        return "/plan/%i/" % self.id

from django.db.models import F
        
class Forecast(models.Model):
    code = models.ForeignKey(Material, on_delete=models.CASCADE)
    month = models.DateField(default=datetime.now)
    version = models.IntegerField()
    fore_qty = models.DecimalField(max_digits=11,decimal_places=2)
    overr_qty = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    dem_month = models.DateField(default=datetime.now)
    def __str__(self):
        return '{} - {} - {}'.format(self.code,self.fore_qty,self.dem_month)
    @property
    def tot_for_qty(self):
      return self.fore_qty + self.overr_qty
    '''
    def get_queryset(self):
        """Overrides the models.Manager method"""
        qs = super(Forecast, self).get_queryset().annotate(tot_for_qty=F(fore_qty)+F(overr_qty))
        return qs
    '''    
class Fmodel(models.Model):
    code = models.ForeignKey(Material, on_delete=models.CASCADE)
    model = models.BinaryField()
    alg = models.CharField(max_length=21,choices=alg_choices)
    smape = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    mae = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    mase = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    def __str__(self):
        return '{} - {}'.format(self.code,self.alg)
        
class Planning(models.Model):
    code = models.ForeignKey(Material, on_delete=models.CASCADE)
    month = models.DateField(default=datetime.now)
    mps_qty = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    pab_qty = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    atp_qty = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)
    def __str__(self):
        return '{} - {}'.format(self.code,self.month)