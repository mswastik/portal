from django.shortcuts import render
from django.http import HttpRequest,HttpResponse
from django.views.generic import ListView,DetailView
from .models import Product,So,Plan,Line
from .admin import SOResource
from django.forms import modelformset_factory,inlineformset_factory
from .tables import SoTable, SoFilter
from django_tables2 import SingleTableView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .forms import SoForm,SoHelper,PlanForm,PlanHelper,LineForm,PlanForm1
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage

# Create your views here.
class SoList(SingleTableMixin,FilterView):
    model = So
    table_class = SoTable
    template_name = 'app1/so_list.html'
    filterset_class = SoFilter

def so_agg(request):
    #assert isinstance(request, HttpRequest)
    ordersrecieved = So.objects.filter(closed=False)
    return render(request,'app1/so_agg.html',{"ordersrecieved": ordersrecieved})

def export(request):
    so_resource = SOResource()
    dataset = so_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="so.csv"'
    return response

def SoView(request):
    Soformset = modelformset_factory(So,form =SoForm,extra=0)
    helper = SoHelper
    query = So.objects.filter(closed=0).order_by('id')
    paginator = Paginator(query, 30) # Show 10 forms per page
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects]).order_by('id')
    if request.method == 'POST':
        formset = Soformset(request.POST)
        if formset.is_valid():
            formset.save()
            formset = Soformset(queryset=page_query.order_by('id'))
            context = {'object': objects, 'formset': formset, 'helper': helper}
            return render(request,'app1/so_form.html',context)
        else:
            formset = Soformset(queryset=page_query.order_by('id'))
            context = {'object': objects, 'formset': formset, 'helper': helper}
            return render(request,'app1/so_form.html',context)
    else:
        formset = Soformset(queryset=page_query)
        context = {'object': objects, 'formset': formset, 'helper': helper}
        return render(request,'app1/so_form.html',context)
    

def SoTableView(SingleTableView):
    Soformset = modelformset_factory(So, fields=('so','so_del_date','code','qty','customer','closed'))
    form = Soformset(queryset=So.objects.filter(closed=0))
    return render(request,'app1/plan.html',{'formset':form})

def index(request):
    model = So
    return render(request,'app1/base.html')

def PlanView(request):
    PlanFormset = modelformset_factory(Plan,fields =('so','date','line'), extra=3)
    #Soformset = SoForm()
    #PlanFormset = PlanForm()
    query = Plan.objects.all()
    helper = PlanForm.helper
    #query = So.objects.all()
    #query = So.objects.filter(closed=0)
    paginator = Paginator(query, 30)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects]).order_by('id')
    if request.method == 'POST':
        formset = PlanFormset(request.POST)
        if formset.is_valid():
            formset.save()
        else:
            formset = PlanFormset(queryset=page_query.order_by('id'))
    else:
        formset = PlanFormset(queryset=page_query.order_by('id'))
    context = {'object': objects, 'formset': formset, 'helper': helper}
    return render(request,'app1/plan.html',context)

def LineView(request):
    LineFormset = modelformset_factory(Line,form =LineForm)
    helper = LineForm.helper
    query = Line.objects.all()
    paginator = Paginator(query, 30)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    page_query = query.filter(id__in=[object.id for object in objects]).order_by('id')
    if request.method == 'POST':
        formset = LineFormset(request.POST)
        if formset.is_valid():
            formset.save()
            formset = LineFormset(queryset=page_query.order_by('id'))
            context = {'object': objects, 'formset': formset,'helper':helper}
            return render(request,'app1/form.html',context)
        else:
            formset = LineFormset(queryset=page_query.order_by('id'))
            context = {'object': objects, 'formset': formset,'helper':helper}
            return render(request,'app1/form.html',context)
    else:
        formset = LineFormset(queryset=page_query)
        context = {'object': objects, 'formset': formset,'helper':helper}
        return render(request,'app1/form.html',context)

def PlanView1(request):
    formset = modelformset_factory(Plan)
    helper = PlanForm1.helper
    if request.method == "POST":
        form = PlanForm1(request.POST)
        if form.is_valid():
            post.save()
            return render(request, 'app1/plan.html', {'form': form,'helper':helper})
    else:
        form = PlanForm1()
    return render(request, 'app1/plan.html', {'form': form,'helper':helper})
