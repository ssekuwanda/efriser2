from django.contrib import admin
from import_export.admin import  ImportExportModelAdmin
from import_export import resources, fields
from .models import *

class MeasurementsResource(resources.ModelResource):
    class Meta:
        model = Unit_Measurement
        fields = ('name','code')

class MeasurementsAdmin(ImportExportModelAdmin):
    resource_class = MeasurementsResource

class TaxTypeResource(resources.ModelResource):
    class Meta:
        model = Tax_Type
        fields = ('__all__')

class TaxTypeAdmin(ImportExportModelAdmin):
    resource_class = TaxTypeResource

admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Settings)
admin.site.register(Unit_Measurement, MeasurementsAdmin)
admin.site.register(CreditNote)
admin.site.register(InvoiceProducts)
admin.site.register(ProductMeta)
admin.site.register(BankDetails)
admin.site.register(CompanyLocation)
admin.site.register(CnCancel)
admin.site.register(Tax_Type,TaxTypeAdmin)