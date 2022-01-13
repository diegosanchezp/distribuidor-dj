from django.contrib import admin

from .models import Invoice, InvoiceStatusDate  # noqa F401

# Register your models here.


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass
