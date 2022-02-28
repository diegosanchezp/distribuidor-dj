"""
Dashboard views
"""

from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment

from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .forms import ShipmentsFilterForm
from .mixins import AdminDashboardPassessTest, DashboardPassesTestMixin


class Index(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/index.html"


class ShipmentsView(DashboardPassesTestMixin, ListView):
    template_name = "dashboard/shipments.html"
    model = Shipment
    paginate_by = 1  # change this later to 10
    extra_context = {
        "filter_form": ShipmentsFilterForm(),
        "shipment_detail_url": "dashboard:shipment-detail",
    }

    def get_context_data(self):
        ctx = super().get_context_data()
        ctx["filter_form"] = ShipmentsFilterForm(data=self.request.GET)
        ctx["statechoices"] = Shipment.States
        return ctx

    def get_queryset(self) -> "QuerySet[Shipment]":
        queryset = super().get_queryset()
        queryset = queryset.filter(commerce=self.request.user)
        queryset = self.apply_search(queryset)
        return queryset

    def apply_search(
        self, queryset: "QuerySet[Shipment]"
    ) -> "QuerySet[Shipment]":
        form = ShipmentsFilterForm(data=self.request.GET)
        if form.is_valid():
            state = form.cleaned_data["state"]
            queryset = queryset.filter(state=state)
        return queryset


class ShipmentDetail(DetailView):
    template_name = "shipments/shipment_detail.html"
    model = Shipment


class InvoicesView(DashboardPassesTestMixin, ListView):
    template_name = "dashboard/invoices.html"
    model = Invoice
    paginate_by = 1  # change this later to 10


class SettingsView(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/settings.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"user": request.user, "request": request},
        )


class InvoiceDetailView(DashboardPassesTestMixin, DetailView):
    template_name = "dashboard/invoice-detail.html"
    model = Invoice
    context_object_name = "invoice"


class ReportesView(AdminDashboardPassessTest, TemplateView):
    template_name = "dashboard/reportes.html"
