from dal import autocomplete
from .models import *
from django.db.models import Q

class ProductAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Product.objects.none()
        qs = Product.objects.all()
        if self.q:
            qs = qs.filter(Q(desc__istartswith=self.q) | Q(code__istartswith=self.q))
        return qs
        
class OpensoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return So.objects.none()
        qs = So.objects.all()
        if self.q:
            qs = qs.filter(Q(closed=False),Q(so__istartswith=self.q) | Q(fgcode__code__istartswith=self.q))
        return qs
    def get_selected_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.fgcode,item.so_qty)
    def get_result_label(self, item):
        return '{} - {} - {}'.format(item.so,item.fgcode,item.so_qty)
        
class SoAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return So.objects.none()
        qs = So.objects.all()
        if self.q:
            qs = qs.filter(Q(so__istartswith=self.q) | Q(fgcode__code__istartswith=self.q))
        return qs
    def get_selected_result_label(self, item):
        return '{}'.format(item.so)
    def get_result_label(self, item):
        return '{}'.format(item.so)
        
class MaterialAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Material.objects.none()
        qs = Material.objects.all()
        if self.q:
            qs = qs.filter(Q(code__istartswith=self.q) | Q(desc__istartswith=self.q))
        return qs
    def get_selected_result_label(self, item):
        return '{} - {}'.format(item.code,item.desc)
    def get_result_label(self, item):
        return '{} - {}'.format(item.code,item.desc)