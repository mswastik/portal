from dal import autocomplete
from .models import *
from django.db.models import Q
from django.db.models.functions import Coalesce
from django.db.models import Sum,Count

class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Material.objects.none()
        qs = Material.objects.filter(classification='FG')
        if self.q:
            qs = qs.filter(Q(desc__icontains=self.q) | Q(code__icontains=self.q))
        return qs
        
class OpensoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = So.objects.all()
        if self.q:
            qs = qs.filter(Q(closed=False),Q(so__icontains=self.q) | Q(code__code__icontains=self.q)| Q(code__desc__icontains=self.q)).order_by('so_del_date')
        return qs
    #def get_selected_result_label(self, item):
    #    return '{} - {} - {}'.format(item.so,item.code,item.so_qty)
    def get_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.code,self.get_queryset().filter(id=item.id).annotate(bal_disp_qty=F('so_qty')-Coalesce(Sum(F('dispatch__dis_qty')),0)).values('bal_disp_qty')[0]['bal_disp_qty'])
        
class SoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return So.objects.none()
        qs = So.objects.all()
        if self.q:
            qs = qs.filter(Q(so__icontains=self.q) | Q(code__code__icontains=self.q))
        return qs
        
    def get_selected_result_label(self, item):
        return '{}'.format(item.so)
    def get_result_label(self, item):
        return '{}'.format(item.so)

#Return SO no. instead of pk
class SoAutocomplete1(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return So.objects.none()
        qs = So.objects.all().distinct('so')
        if self.q:
            qs = qs.filter(Q(so__icontains=self.q) | Q(code__code__icontains=self.q)).distinct('so')
        return qs
    #def get_result_value(self, result):
        """Return the value of a result."""
    #    return '{} - {} - {}'.format(result.so,result.fgcode,result.so_qty) #change pk to the variable of your choice
        
    def get_selected_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.code,item.so_qty)
    def get_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.code,item.so_qty)        
        
class MaterialAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Material.objects.none()
        qs = Material.objects.all()
        if self.q:
            qs = qs.filter(Q(code__icontains=self.q) | Q(desc__icontains=self.q))
        return qs
    def get_selected_result_label(self, item):
        return '{} - {}'.format(item.code,item.desc)
    def get_result_label(self, item):
        return '{} - {}'.format(item.code,item.desc)


class OpenprodsoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        qs = So.objects.all()
        if self.q:
            qs = qs.filter(Q(closed=False),Q(so__icontains=self.q) | Q(code__code__icontains=self.q)).order_by('so_del_date')
        return qs
    #def get_selected_result_label(self, item):
    #    return '{} - {} - {}'.format(item.so,item.code,self.q.bal_prod_qty)
    def get_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.code,self.get_queryset().filter(id=item.id).annotate(bal_prod_qty=F('so_qty')-Coalesce(Sum(F('production__prod_qty')),0)).values('bal_prod_qty')[0]['bal_prod_qty'])
