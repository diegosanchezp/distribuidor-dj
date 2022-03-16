from django.contrib import admin

from .models import Invoice, InvoiceStatusDate


# Register your models here.
class InvoiceStatusDateInline(admin.TabularInline):
    model = InvoiceStatusDate
    extra = 2


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("commerce", "state")
    inlines = (InvoiceStatusDateInline,)


@admin.register(InvoiceStatusDate)
class InvoiceStatusDateAdmin(admin.ModelAdmin):
    list_display = ("invoice", "status", "date")
