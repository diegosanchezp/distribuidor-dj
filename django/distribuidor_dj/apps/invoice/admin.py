from django.contrib import admin

from .models import Invoice, InvoiceStatusDate


# Register your models here.
class InvoiceStatusDateInline(admin.TabularInline):
    model = InvoiceStatusDate
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (InvoiceStatusDateInline,)
