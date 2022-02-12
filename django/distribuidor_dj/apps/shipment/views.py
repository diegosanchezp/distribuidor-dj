# Create your views here.
from distribuidor_dj.apps.dashboard.mixins import AdminDashboardPassessTest
from distribuidor_dj.apps.dashboard.views import ShipmentsView

from django.db.models.query import QuerySet
from django.shortcuts import render  # noqa F01

from .models import Shipment


class AdminDashShipmentList(AdminDashboardPassessTest, ShipmentsView):
    template_name = "dashboard/shipments.html"
    paginate_by = 2  # change this later to 10

    def get_queryset(self) -> "QuerySet[Shipment]":
        queryset = Shipment.objects.all()
        queryset = self.apply_search(queryset)
        return queryset
