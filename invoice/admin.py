from django.contrib import admin
from .models import *
admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Settings)
admin.site.register(Unit_Measurement)

admin.site.register(InvoiceProducts)



