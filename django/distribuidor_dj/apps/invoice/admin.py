from django.contrib import admin
from django.urls.base import reverse
from django.utils.html import format_html

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
    list_display = ("id", "my_invoice", "status", "date")

    @admin.display(description="invoice")
    def my_invoice(self, status_date: "Invoice"):
        url = reverse(
            "admin:invoice_invoice_change", args=(status_date.invoice.id,)
        )
        return format_html(f'<a href="{url}">{status_date.invoice.id}</a>')
