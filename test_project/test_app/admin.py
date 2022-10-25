from django.contrib import admin

# Register your models here.
from test_app.models import (Product, Order)


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "description", "created_at")
    search_fields = ["name", "description"]


class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "customer_name", "created_at")
    search_fields = ["product", "customer_name"]


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
