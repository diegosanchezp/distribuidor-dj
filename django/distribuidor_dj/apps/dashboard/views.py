"""
Dashboard views
"""
from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment

from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .mixins import DashboardPassesTestMixin


class Index(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/index.html"


class ShipmentsView(DashboardPassesTestMixin, ListView):
    template_name = "dashboard/shipments.html"
    model = Shipment
    paginate_by = 1  # change this later to 10


class InvoicesView(DashboardPassesTestMixin, ListView):
    template_name = "dashboard/invoices.html"
    model = Invoice
    paginate_by = 1  # change this later to 10


class SettingsView(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/settings.html"


class TrackingView(DashboardPassesTestMixin, TemplateView):
    template_name = "tracking/index.html"


class TrackingResultView(DashboardPassesTestMixin, TemplateView):
    template_name = "tracking/result.html"


class InvoiceDetailView(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/invoice-detail.html"
