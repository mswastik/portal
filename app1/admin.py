from import_export import resources,fields

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
#from ra.admin.admin import ra_admin_site, EntityAdmin, TransactionAdmin, TransactionItemAdmin

# Register your models here.
from .models import Product,So,Calendar,BOM,Stock,StockFG,Material,Production,Line,Speed,Plan,Customer

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product
        exclude = ()
        skip_unchanged = True
        report_skipped = True
        import_id_fields = ('code',)

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

class StockFGResource(resources.ModelResource):
    class Meta:
        model = StockFG
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

class SpeedResource(resources.ModelResource):
    line = fields.Field(column_name='line',attribute='line',widget=ForeignKeyWidget(Line, 'line'))
    class Meta:
        model = Speed
        fields = ('id', 'code', 'line','speed')
        skip_unchanged = True
        report_skipped = True

    

class ProductAdmin(ImportExportModelAdmin):
    resource_class = ProductResource

class SOAdmin2(ImportExportModelAdmin):
    resource_class =SOResource

class CalendarAdmin(ImportExportModelAdmin):
    resource_class = CalendarResource

class BOMAdmin(ImportExportModelAdmin):
    resource_class = BOMResource

class StockFGAdmin(ImportExportModelAdmin):
    resource_class = StockFGResource

class StockAdmin(ImportExportModelAdmin):
    resource_class = StockResource

class MaterialAdmin(ImportExportModelAdmin):
    resource_class = MaterialResource

class ProductionAdmin(ImportExportModelAdmin):
    resource_class = ProductionResource
    
class LineAdmin(ImportExportModelAdmin):
    resource_class = LineResource

class PlanAdmin(ImportExportModelAdmin):
    resource_class = PlanResource

class SpeedAdmin(ImportExportModelAdmin):
    resource_class = SpeedResource

class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource

admin.site.register(Product,ProductAdmin)
admin.site.register(Production,ProductionAdmin)
admin.site.register(So,SOAdmin2)
admin.site.register(Calendar,CalendarAdmin)
admin.site.register(BOM,BOMAdmin)
admin.site.register(StockFG,StockFGAdmin)
admin.site.register(Stock,StockAdmin)
admin.site.register(Material,MaterialAdmin)
admin.site.register(Speed,SpeedAdmin)
admin.site.register(Line,LineAdmin)
admin.site.register(Plan,PlanAdmin)
admin.site.register(Customer,CustomerAdmin)
