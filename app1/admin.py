from import_export import resources,fields

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
#from ra.admin.admin import ra_admin_site, EntityAdmin, TransactionAdmin, TransactionItemAdmin

# Register your models here.
from .models import So,Calendar,BOM,Stock,Material,Production,Line,Speed,Plan,Customer,Dispatch,WCGroup,Routing,Forecast,Fmodel


class SOResource(resources.ModelResource):
    class Meta:
        model = So
        skip_unchanged = True
        report_skipped = True

class CalendarResource(resources.ModelResource):
    class Meta:
        model = Calendar
        skip_unchanged = True
        report_skipped = True

class LineResource(resources.ModelResource):
    class Meta:
        model = Line
        skip_unchanged = True
        report_skipped = True

class PlanResource(resources.ModelResource):
    class Meta:
        model = Plan
        skip_unchanged = True
        report_skipped = True

class BOMResource(resources.ModelResource):
    class Meta:
        model = BOM
        skip_unchanged = True
        report_skipped = True

class StockResource(resources.ModelResource):
    class Meta:
        model = Stock
        skip_unchanged = True
        report_skipped = True
        
class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
        skip_unchanged = True
        report_skipped = True
        
class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer
        skip_unchanged = True
        report_skipped = True
        
class ProductionResource(resources.ModelResource):
    class Meta:
        model = Production
        skip_unchanged = True
        report_skipped = True

class DispatchResource(resources.ModelResource):
    class Meta:
        model = Dispatch
        skip_unchanged = True
        report_skipped = True
        
class WCGroupResource(resources.ModelResource):
    class Meta:
        model = WCGroup
        skip_unchanged = True
        report_skipped = True

class RoutingResource(resources.ModelResource):
    class Meta:
        model = Routing
        skip_unchanged = True
        report_skipped = True

class ForecastResource(resources.ModelResource):
    class Meta:
        model = Forecast
        skip_unchanged = True
        report_skipped = True

class FmodelResource(resources.ModelResource):
    class Meta:
        model = Fmodel
        skip_unchanged = True
        report_skipped = True

class SpeedResource(resources.ModelResource):
    line = fields.Field(column_name='line',attribute='line',widget=ForeignKeyWidget(Line, 'line'))
    class Meta:
        model = Speed
        fields = ('id', 'code', 'line','speed')
        skip_unchanged = True
        report_skipped = True

class SOAdmin2(ImportExportModelAdmin):
    resource_class =SOResource

class CalendarAdmin(ImportExportModelAdmin):
    resource_class = CalendarResource

class BOMAdmin(ImportExportModelAdmin):
    resource_class = BOMResource

class StockAdmin(ImportExportModelAdmin):
    resource_class = StockResource

class MaterialAdmin(ImportExportModelAdmin):
    resource_class = MaterialResource

class ProductionAdmin(ImportExportModelAdmin):
    resource_class = ProductionResource

class DispatchAdmin(ImportExportModelAdmin):
    resource_class = DispatchResource

class LineAdmin(ImportExportModelAdmin):
    resource_class = LineResource

class PlanAdmin(ImportExportModelAdmin):
    resource_class = PlanResource

class SpeedAdmin(ImportExportModelAdmin):
    resource_class = SpeedResource

class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource

class WCGroupAdmin(ImportExportModelAdmin):
    resource_class = WCGroupResource

class RoutingAdmin(ImportExportModelAdmin):
    resource_class = RoutingResource
    
class ForecastAdmin(ImportExportModelAdmin):
    resource_class = ForecastResource    
 
class FmodelAdmin(ImportExportModelAdmin):
    resource_class = FmodelResource 
 
admin.site.register(Production,ProductionAdmin)
admin.site.register(Dispatch,DispatchAdmin)
admin.site.register(So,SOAdmin2)
admin.site.register(Calendar,CalendarAdmin)
admin.site.register(BOM,BOMAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(Speed,SpeedAdmin)
admin.site.register(Line,LineAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Customer,CustomerAdmin)
admin.site.register(WCGroup,WCGroupAdmin)
admin.site.register(Routing,RoutingAdmin)
admin.site.register(Forecast,ForecastAdmin)
admin.site.register(Fmodel,FmodelAdmin)