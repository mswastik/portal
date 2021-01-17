from django.db import models
#from annoying.fields import AutoOneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _

shift_choices = (("A", "A"),("B", "B"),("C", "C"),
)

plant_choices = (("1024", "1024"),("1025", "1025"),
)

curr_choices = (
("USD", "USD"),
 ("EUR", "EUR"),("INR", "INR"),
)


# Create your models here.

class Product(models.Model):
    code = models.CharField(max_length=15,unique=True,primary_key=True,verbose_name='Code')
    desc = models.CharField(max_length=60,verbose_name='Description')
    case_size = models.IntegerField(blank=True,null=True,verbose_name='Description')
    bulk_code = models.CharField(max_length=7,verbose_name='Description')
    micro = models.BooleanField(blank=True,null=True,verbose_name='Description')
    carton = models.BooleanField(blank=True,null=True,verbose_name='Description')
    #stripe = models.BooleanField()
    bus_category = models.CharField(max_length=15,blank=True,null=True,verbose_name='Description')
    prod_category = models.CharField(max_length=25,verbose_name='Description')
    gr_wt = models.DecimalField(max_digits=9,decimal_places=4,blank=True,null=True,verbose_name='Description')
    nt_wt = models.DecimalField(max_digits=9,decimal_places=4,blank=True,null=True,verbose_name='Description')
    plant = models.CharField(max_length=4,choices=plant_choices,verbose_name='Description')
    line_bulk = models.CharField(max_length=25,blank=True,null=True,verbose_name='Description')
    des_code = models.CharField(max_length=15,blank=True,null=True,verbose_name='Description')
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
    def __str__(self):              # __unicode__ on Python 2
        return self.desc


class So(models.Model):
    so = models.CharField(max_length=25,verbose_name='SO')
    so_date = models.DateTimeField(verbose_name='SO')
    so_del_date = models.DateTimeField(verbose_name='SO')
    code = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,verbose_name='Code')
    qty = models.DecimalField(default=0,max_digits=7,decimal_places=1,verbose_name='Quantity')
    closed = models.BooleanField(verbose_name='SO')
    act_disp_qty = models.IntegerField(default=0,verbose_name='SO')
    act_disp_date = models.DateTimeField(null=True,blank=True,verbose_name='SO')
    rate = models.DecimalField(max_digits=5,decimal_places=2,null=True,verbose_name='SO')
    currency = models.CharField(max_length=3,choices=curr_choices,null=True,verbose_name='SO')
    customer = models.CharField(max_length=35,verbose_name='SO')
    '''class Meta:
        verbose_name = _('So')
        verbose_name_plural = _('Sos')'''
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {} - {} - {}'.format(self.so,self.customer,self.code,self.qty)
    def get_absolute_url(self):
        return "/app1/sodetail/%i" % self.id
    

class Calendar(models.Model):
    date = models.DateTimeField()
    working = models.BooleanField()
    def __str__(self):              # __unicode__ on Python 2
        return self.date

class Material(models.Model):
    code = models.CharField(max_length=12,primary_key=True)
    desc = models.CharField(max_length=35)
    rate = models.DecimalField(max_digits=7,decimal_places=2)
    uom = models.CharField(max_length=3)
    lead_time = models.IntegerField(default=0)
    classification = models.CharField(max_length=10)
    def __str__(self):              # __unicode__ on Python 2
        return self.desc

class BOM(models.Model):
    code = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    material_code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True,to_field='code')
    qty = models.DecimalField(max_digits=9,decimal_places=4)
    uom = models.CharField(max_length=3)
    active = models.BooleanField()
    def __str__(self):              # __unicode__ on Python 2
        return self.code

class StockFG(models.Model):
    material_code = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    qty_released = models.DecimalField(max_digits=9,decimal_places=2)
    qty_quality = models.DecimalField(max_digits=9,decimal_places=2)
    uom = models.CharField(max_length=3)
    #def __str__(self):              # __unicode__ on Python 2
    #    return str(material_code,self.qty_released)

class Stock(models.Model):
    material_code = models.ForeignKey(Material,on_delete=models.SET_NULL,null=True)
    qty_released = models.DecimalField(max_digits=9,decimal_places=2)
    qty_quality = models.DecimalField(max_digits=9,decimal_places=2)
    uom = models.CharField(max_length=3)
    #def __str__(self):              # __unicode__ on Python 2
    #    return self.material_code

class Line(models.Model):
    line = models.CharField(max_length=3,unique=True)
    #line = models.CharField(max_length=15)
    def __str__(self):              # __unicode__ on Python 2
        return self.line
        
class Production(models.Model):
    code = models.ForeignKey(Product, on_delete=models.CASCADE)
    line = models.ForeignKey(Line,on_delete=models.SET_NULL,null=True)
    date = models.DateField()
    shift = models.CharField(max_length=1,choices=shift_choices)
    qty = models.DecimalField(max_digits=7,decimal_places=2)
    doc_date = models.DateField(auto_now=True)
    def __str__(self):              # __unicode__ on Python 2
        return '{}'.format(self.qty)



class Speed(models.Model):
    code = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True,to_field='code')
    line = models.ForeignKey(Line,on_delete=models.SET_NULL,null=True,to_field='line')
    speed = models.FloatField()
    def __str__(self):              # __unicode__ on Python 2
        return str(self.speed)

class Plan(models.Model):
    so = models.ForeignKey(So,on_delete=models.CASCADE, null=True,to_field='id', related_name='plan')
    #so = AutoOneToOneField(So,on_delete=models.CASCADE,primary_key=True)
    date = models.DateTimeField(null=True,blank=True)
    line = models.ForeignKey(Line,on_delete=models.SET_NULL,blank=True,null=True,to_field='line')
    plan_qty = models.IntegerField()
    def __str__(self):              # __unicode__ on Python 2
        return '{} - {} - {}'.format(self.so,self.date,self.line)
    def get_absolute_url(self):
        return "/plan/%i/" % self.id
    #def save(self, *args, **kwargs):
    #    if self.qty is null:
    #        self.qty = self.so.qty
    #    super(Plan, self).save(*args, **kwargs)
    #@receiver(post_save, sender=So)
    #def create_member(sender, instance, created, **kwargs):
    #    if created:
    #        Plan.objects.create(so=instance)