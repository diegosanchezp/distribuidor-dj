"""
Dashboard views
"""

from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment
from django_htmx.http import trigger_client_event

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from . import forms as dash_forms
from .forms import BaseDateFilterFormChoices, ShipmentsFilterForm
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


# Querys
def solicitudes_despachadas_pendientes_dia(form):
    # Obtener fecha especificada por defecto
    # si el formulario no esta rellenado
    fecha_especificada = form.fields["dia"].initial
    if form.is_valid():
        fecha_especificada = form.cleaned_data["dia"]

        # Obtener numero solictudes pendientes por despachar
        # en el dia especificado de tiempo
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            dates__date__date=fecha_especificada,
        ).count()

        # Obtener numero solictudes despachadas
        # en el dia especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            dates__date__date=fecha_especificada,
        ).count()

        # Hacer calculos de porcentajes
        # 1. Despachadas
        p_pendientes = n_pendientes
        p_despachadas = n_despachadas

        # Retornar data ajustada a chart.js
        return (
            p_pendientes,
            p_despachadas,
        )


def solicitudes_despachadas_pendientes_mes(form):
    pass


def solicitudes_despachadas_pendientes_rango(form):
    pass


class ReportesView(AdminDashboardPassessTest, FormView):
    template_name = "dashboard/reportes.html"

    form_class = dash_forms.BaseDateFilterForm  # Root form class
    forms_config = {
        BaseDateFilterFormChoices.DIA: {
            "class": dash_forms.ChartDateDayFilterForm,
            "name": "day_form",
            "query": solicitudes_despachadas_pendientes_dia,
            "chartName": "despachadasPendientes",
        },
        BaseDateFilterFormChoices.MES: {
            "class": dash_forms.ChartDateMonthFilterForm,
            "name": "month_form",
        },
        BaseDateFilterFormChoices.INTERVALO: {
            "class": dash_forms.ChartDateRangeFilterForm,  # noqa: E501, E261
            "name": "range_form",
        },
    }

    extra_context = {"datechoices": dash_forms.BaseDateFilterFormChoices}

    def get(self, request, *args, **kwargs):
        # TODO: define default chart to render when no query params

        # No query params do normal get flow
        if not len(self.request.GET) > 0 and not self.request.htmx:
            return super().get(request, *args, **kwargs)

        f = self.form_class(data=self.request.GET)
        if not f.is_valid():
            return self.form_invalid(form=f)

        # Get the child form class and construct the form
        child_form_config = self.forms_config[f.cleaned_data.get("tipo")]

        actual_form = child_form_config["class"](
            data=self.request.GET
            # data={"tipo": "dia","dia": "aaaaa"}
        )

        if not actual_form.is_valid():

            data = {
                child_form_config["name"]: actual_form.errors,
            }

            res = JsonResponse(
                data=data,
                status=400,
            )
            return res

        query_data = child_form_config["query"](actual_form)

        # queryset = self.get_query()
        # Convert query to json

        # This should be an htmx response

        res = HttpResponse()
        trigger_client_event(
            response=res,
            name="createnewchart",
            params={
                "data": query_data,
                "chartName": child_form_config["chartName"],
            },
        )
        return res

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        # TODO: querys por defecto
        if "day_form" not in kwargs:
            ctx["day_form"] = dash_forms.ChartDateDayFilterForm()
        if "month_form" not in kwargs:
            ctx["month_form"] = dash_forms.ChartDateMonthFilterForm()
        if "range_form" not in kwargs:
            ctx["range_form"] = dash_forms.ChartDateRangeFilterForm()
        return ctx

    def get_query(self):
        # tipo = form.cleaned_data.get("tipo")
        pass

    # Fatan mas de 9 Querys...
