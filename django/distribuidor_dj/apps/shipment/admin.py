from django.contrib import admin

from .models import (
    Address,
    AddressState,
    Product,
    ProductQuantity,
    Shipment,
    ShipmentStatusDate,
)


class ProductQuantityInline(admin.TabularInline):
    model = ProductQuantity
    extra = 1


class ShipmentStatusDateInline(admin.StackedInline):
    model = ShipmentStatusDate
    extra = 1
    fields = ("status",)


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


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("state", "city", "street", "zipcode")

    @admin.display()
    def state(self, obj: AddressState):
        return obj.name


admin.site.register(Product)
admin.site.register(AddressState)
