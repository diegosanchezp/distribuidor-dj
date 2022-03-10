"""
Dashboard views
"""

import requests
from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment

from django.conf import settings
from django.db.models.query import QuerySet
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, UpdateView
from django.views.generic.list import ListView

from .forms import DakitiForm, ShipmentsFilterForm
from .mixins import AdminDashboardPassessTest, DashboardPassesTestMixin


class Index(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/index.html"


class Payments(TemplateView):
    template_name = "dashboard/payments.html"


class ShipmentsView(DashboardPassesTestMixin, ListView):
    template_name = "dashboard/shipments.html"
    model = Shipment
    paginate_by = 10  # change this later to 10
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
    paginate_by = 10


class SettingsView(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/settings.html"

    def get(self, request, *args, **kwargs):
        return render(
            request,
            self.template_name,
            {"user": request.user, "request": request},
        )


class InvoiceDetailView(DashboardPassesTestMixin, UpdateView):
    template_name = "dashboard/invoice-detail.html"
    model = Invoice
    context_object_name = "invoice"
    form_class = DakitiForm
    extra_context = {"states": Invoice.States}

    def get_form_kwargs(self):
        return FormMixin.get_form_kwargs(self)

    def form_valid(self, form):
        invoice: "Invoice" = self.object

        # Api key de prueba
        # "apiKey": "71b86b25305c5ae6028e0d6060658e3d9862a06d",
        res_data = form.cleaned_data | {
            # Api key real la de mi usuario juridico
            "apiKey": settings.DAKITI_API_KEY,
            "monto": invoice.ammount,
            "descripcion": f"Pago Factura {invoice.id}",
            "nombre": self.request.user.username,
        }

        payment_res = requests.post(
            url="https://dakiti-back.herokuapp.com/api/testcards",
            json=res_data,
        )
        # Todo refactor this horrible code

        # Foward error messages
        if payment_res.status_code == 400:
            if res_json := payment_res.json():
                message = {"error": res_json.get("message")}
            else:
                message = {
                    "error": "Servicio de pagos de Dakiti no disponible",
                }
            return JsonResponse(data=message, status=payment_res.status_code)

        if payment_res.status_code == 200:
            res_json = payment_res.json()
            # Update the invoice state to payed
            status_date = invoice.transition_set_date(Invoice.Events.ON_PAY)
            status_date.save()
            invoice.save()
            return JsonResponse(
                data={
                    "success": res_json.get("message"),
                },
                status=payment_res.status_code,
            )


class ReportesView(AdminDashboardPassessTest, TemplateView):
    template_name = "dashboard/reportes.html"
