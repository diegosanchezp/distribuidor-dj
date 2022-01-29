"""
Dashboard views
"""
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
