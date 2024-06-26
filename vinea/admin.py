from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'volume', 'sale_price', 'purchase_price', 'on_hand', 'group', 'supplier')

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'order_date', 'reception_date', 'purchase_price', 'quantity', 'total_price', 'item', 'supplier')
@admin.register(Suppliers)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_name', 'contact', 'address', 'email')

@admin.register(Sales)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('quantity', 'unit_price', 'date', 'item')


