from dal import autocomplete
from .models import *
from django.db.models import Q

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
        if not self.request.user.is_authenticated:
            return So.objects.none()
        qs = So.objects.all()
        if self.q:
            qs = qs.filter(Q(closed=False),Q(so__icontains=self.q) | Q(code__code__icontains=self.q))
        return qs
    def get_selected_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.code,item.so_qty)
    def get_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.code,item.so_qty)
        
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