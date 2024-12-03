from django.contrib import admin
from.models import OrderDetails,OrderItemMapping
from .utils import export_as_csv


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ('id', 'userid', 'address', 'paymenttype', 'status', 'date')
    actions = [export_as_csv] 

class OrderItemMappingAdmin(admin.ModelAdmin):
    list_display = ('id', 'orderDetails', 'itemDetails', 'quantity', 'amount')
    actions = [export_as_csv]  

admin.site.register(OrderDetails, OrderDetailsAdmin)
admin.site.register(OrderItemMapping, OrderItemMappingAdmin)