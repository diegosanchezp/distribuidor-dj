from django.contrib import admin  # noqa F401

from .models import (
    Address,
    Product,
    ProductQuantity,
    Shipment,
    ShipmentStatusDate,
)


class ProductQuantityInline(admin.TabularInline):
    model = ProductQuantity
    extra = 1


class ShipmentStatusDateInline(admin.TabularInline):
    model = ShipmentStatusDate
    extra = 1


# Register your models here.
@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    inlines = (ProductQuantityInline, ShipmentStatusDateInline)


admin.site.register(Product)
admin.site.register(Address)
