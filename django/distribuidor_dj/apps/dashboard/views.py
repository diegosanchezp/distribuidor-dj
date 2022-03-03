"""
Dashboard views
"""
from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment
from django_htmx.http import trigger_client_event

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.utils import timezone
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
    if form.is_valid():
        month = form.cleaned_data["month"]
        # Obtener numero solictudes pendientes por despachar
        # en el mes/añi especificado de tiempo
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            dates__date__month=month,
            dates__date__year=timezone.now().year,
        ).count()

        # Obtener numero solictudes despachadas
        # en el mes/año especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            dates__date__month=month,
            dates__date__year=timezone.now().year,
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


def solicitudes_despachadas_pendientes_rango(form):
    if form.is_valid():
        initial_date = form.cleaned_data["initial_date"]
        end_date = form.cleaned_data["end_date"]

        # Obtener numero solictudes pendientes por despachar
        # en el rango especificado de tiempo
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            dates__date__range=[initial_date, end_date],
        ).count()

        # Obtener numero solictudes despachadas
        # en el rango especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            dates__date__range=[initial_date, end_date],
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


def facturas_vigentes_vencidas_dia(form):
    # Obtener fecha especificada por defecto
    # si el formulario no esta rellenado
    fecha_especificada = form.fields["dia"].initial
    if form.is_valid():
        fecha_especificada = form.cleaned_data["dia"]

        # Obtener numero facturas vigentes pendientes por cobrar
        # en el dia especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__date__gte=timezone.now(),
            dates__date__date=fecha_especificada,
        ).count()

        # Obtener numero facturas vencidas pendientes por cobrar
        # en el dia especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__date__lt=timezone.now(),
            dates__date__date=fecha_especificada,
        ).count()

        # Hacer calculos de porcentajes
        # 1. Vigentes
        p_vigentes = n_vigentes
        p_vencidas = n_vencidas

        # Retornar data ajustada a chart.js
        return (
            p_vigentes,
            p_vencidas,
        )


def facturas_vigentes_vencidas_mes(form):
    if form.is_valid():
        month = form.cleaned_data["month"]
        # Obtener numero solictudes pendientes por despachar
        # en el mes/año especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__month__gte=month,
            dates__date__year__gte=timezone.now().year,
            dates__date__date__gte=timezone.now(),
        ).count()

        # Obtener numero solictudes despachadas
        # en el mes/año especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__month=month,
            dates__date__year=timezone.now().year,
            dates__date__date__lt=timezone.now(),
        ).count()

        # Hacer calculos de porcentajes
        # 1. Despachadas
        p_vigentes = n_vigentes
        p_vencidas = n_vencidas

        # Retornar data ajustada a chart.js
        return (p_vigentes, p_vencidas)


def facturas_vigentes_vencidas_rango(form):
    if form.is_valid():
        initial_date = form.cleaned_data["initial_date"]
        end_date = form.cleaned_data["end_date"]
        # Obtener numero solictudes pendientes por despachar
        # en el mes/año especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__range=[timezone.now(), end_date],
        ).count()

        # Obtener numero solictudes despachadas
        # en el mes/año especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__range=[initial_date, timezone.now()],
        ).count()

        # Hacer calculos de porcentajes
        # 1. Despachadas
        p_vigentes = n_vigentes
        p_vencidas = n_vencidas

        # Retornar data ajustada a chart.js
        return (p_vigentes, p_vencidas)


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
            "query": solicitudes_despachadas_pendientes_mes,
            "chartName": "despachadasPendientes",
        },
        BaseDateFilterFormChoices.INTERVALO: {
            "class": dash_forms.ChartDateRangeFilterForm,  # noqa: E501, E261
            "name": "range_form",
            "query": solicitudes_despachadas_pendientes_rango,
            "chartName": "despachadasPendientes",
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
