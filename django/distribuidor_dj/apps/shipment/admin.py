from django.contrib import admin

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
    list_display = ("commerce", "state", "date")
    list_filter = ("state",)
    inlines = (ProductQuantityInline, ShipmentStatusDateInline)

    @admin.display()
    def date(self, obj: Shipment) -> str:
        date = obj.get_current_status_date()
        if date is None:
            return "-"
        return str(date)


admin.site.register(Product)
admin.site.register(Address)
