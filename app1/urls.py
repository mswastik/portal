"""proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import ListView,TemplateView
#from .views import SoList,index,SoUpdate,ProductUpdate,planpivot,ProductionCreate,DispatchCreate,SoCreate,SoDetail,SpeedCreate,sopivot1,ProductCreate,ProductDetail,sodview,sopivot,LineCreate,WPList,visualization,PlanList,ProductionList,SpeedList,ProductList,MaterialList,BOMList
from django.conf.urls import url
from .views import *
from django_filters.views import FilterView
from .autocomplete import *
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()

urlpatterns = [
    path('', index, name='index'),
    url(r'^product-autocomplete/$',ProductAutocomplete.as_view(),name='product-autocomplete',),
    url(r'^openso-autocomplete/$',OpensoAutocomplete.as_view(),name='openso-autocomplete',),
    url(r'^so-autocomplete/$',SoAutocomplete.as_view(),name='so-autocomplete',),
    url(r'^so-autocomplete1/$',SoAutocomplete1.as_view(),name='so-autocomplete1',),
    url(r'^material-autocomplete/$',MaterialAutocomplete.as_view(),name='material-autocomplete',),
    #path(r'select2/', include('django_select2.urls')),
    path('solist/', SoList.as_view(), name='solist'),
    path('wplist/', WPList.as_view(), name='wplist'),
    path('planlist/', PlanList.as_view(), name='planlist'),
    path('speedlist/', SpeedList.as_view(), name='speedlist'),
    path('productlist/', ProductList.as_view(), name='productlist'),
    path('materiallist/', MaterialList.as_view(), name='materiallist'),
    path('dispatchlist/', DispatchList.as_view(), name='dispatchlist'),
    path('bomlist/', BOMList.as_view(), name='bomlist'),
    path('productionlist/', ProductionList.as_view(), name='productionlist'),
    path('customerlist/', CustomerList.as_view(), name='customerlist'),
    path('soform/', SoCreate, name='soform'),
    path('lineform/', LineCreate, name='lineform'),
    path('productform/', ProductCreate, name='productform'),
    path('lineform/', LineCreate, name='lineform'),
    path('speedform/', SpeedCreate, name='speedform'),
    path('productionform/', ProductionCreate, name='productionform'),
    path('dispatchform/', DispatchCreate, name='dispatchform'),
    path('customerform/', CustomerCreate, name='customerform'),
    path('bomform/', BOMCreate, name='bomform'),
    path('materialform/', MaterialCreate, name='materialform'),
    path('soupdate/', SoUpdate, name='soupdate'),
    path('productupdate/', ProductUpdate, name='productupdate'),
    path('dispatchupdate/', DispatchUpdate, name='dispatchupdate'),
    path('productionupdate/', ProductionUpdate, name='productionupdate'),
    path('sodetail/<int:pk>', SoDetail.as_view(), name='sodetail'),
    path('productdetail/<int:pk>', ProductDetail.as_view(), name='productdetail'),
    path('productiondetail/<int:pk>', ProductionDetail.as_view(), name='productiondetail'),
    path('materialdetail/<int:pk>', MaterialDetail.as_view(), name='materialdetail'),
    path('dispatchdetail/<int:pk>', DispatchDetail.as_view(), name='dispatchdetail'),
    path('bomdetail/<int:fgcode_id>', BOMDetail, name='bomdetail'),
    path('matreq', matreq, name='matreq'),
    path('openso', openso, name='openso'),
    path('plotly/', visualization, name='plotly'),
    path('sopivot/', sopivot, name='sopivot'),
    path('prodpivot/', prodpivot, name='prodpivot'),
    path('planpivot/', planpivot, name='planpivot'),
    path('matreqpivot/', matreqpivot, name='matreqpivot'),
    path('sodview/',sodview,name='sodview'),
    #path('django_plotly_dash/', include('django_plotly_dash.urls')),
]
