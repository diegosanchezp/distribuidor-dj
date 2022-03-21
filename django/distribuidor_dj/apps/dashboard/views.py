"""
Dashboard views
"""


import requests
from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment
from django_htmx.http import trigger_client_event

from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormMixin, FormView, UpdateView
from django.views.generic.list import ListView

from . import forms as dash_forms
from .forms import (
    BaseDateFilterFormChoices,
    ChartTypeChoices,
    DakitiForm,
    ShipmentsFilterForm,
)
from .mixins import (
    AdminDashboardPassessTest,
    DashboardPassesTestMixin,
    InvoiceDetailTest,
    ShipmentDetailTest,
)
from .querys import (
    facturas_ordenadas_fecha_cancelacion_dia,
    facturas_ordenadas_fecha_cancelacion_mes,
    facturas_ordenadas_fecha_cancelacion_rango,
    facturas_vigentes_vencidas_dia,
    facturas_vigentes_vencidas_mes,
    facturas_vigentes_vencidas_rango,
    solicitudes_despachadas_pendientes_dia,
    solicitudes_despachadas_pendientes_mes,
    solicitudes_despachadas_pendientes_rango,
)


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


class ShipmentDetail(ShipmentDetailTest, DetailView):
    template_name = "shipments/admin_shipment_detail.html"
    slug_field = "id"
    model = Shipment
    extra_context = {
        "statechoices": Shipment.States,
    }


class InvoicesView(DashboardPassesTestMixin, ListView):
    template_name = "dashboard/invoices.html"
    model = Invoice
    paginate_by = 10

    def get_queryset(self) -> "QuerySet[Invoice]":
        queryset = super().get_queryset()
        queryset = queryset.filter(commerce=self.request.user)
        return queryset


class SettingsView(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/settings.html"


class InvoiceDetailView(InvoiceDetailTest, UpdateView):
    template_name = "dashboard/invoice-detail.html"
    model = Invoice
    context_object_name = "invoice"
    form_class = DakitiForm
    extra_context = {"states": Invoice.States}

    def get_form_kwargs(self):
        return FormMixin.get_form_kwargs(self)

    def get_object(self, queryset=None):
        if order := self.request.GET.get("order"):
            if queryset is None:
                queryset = self.get_queryset()
            invoice = Invoice.objects.get(id=order)
            return invoice
        return super().get_object(queryset)

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


class ReportesView(AdminDashboardPassessTest, FormView):
    template_name = "dashboard/reportes.html"

    form_class = dash_forms.BaseDateFilterForm  # Root form class
    forms_config = {
        ChartTypeChoices.ENVIOS: {
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
        },
        ChartTypeChoices.CLIENTES: {
            BaseDateFilterFormChoices.DIA: {
                "class": dash_forms.ChartDateDayFilterForm,
                "name": "day_form",
                "query": facturas_vigentes_vencidas_dia,
                "chartName": "facturasVigentes",
            },
            BaseDateFilterFormChoices.MES: {
                "class": dash_forms.ChartDateMonthFilterForm,
                "name": "month_form",
                "query": facturas_vigentes_vencidas_mes,
                "chartName": "facturasVigentes",
            },
            BaseDateFilterFormChoices.INTERVALO: {
                "class": dash_forms.ChartDateRangeFilterForm,  # noqa: E501, E261
                "name": "range_form",
                "query": facturas_vigentes_vencidas_rango,
                "chartName": "facturasVigentes",
            },
        },
        ChartTypeChoices.DESTINOS: {
            BaseDateFilterFormChoices.DIA: {
                "class": dash_forms.ChartDateDayFilterForm,
                "name": "day_form",
                "query": facturas_vigentes_vencidas_dia,
                "chartName": "facturasVigentes",
            },
            BaseDateFilterFormChoices.MES: {
                "class": dash_forms.ChartDateMonthFilterForm,
                "name": "month_form",
                "query": facturas_vigentes_vencidas_mes,
                "chartName": "facturasVigentes",
            },
            BaseDateFilterFormChoices.INTERVALO: {
                "class": dash_forms.ChartDateRangeFilterForm,  # noqa: E501, E261
                "name": "range_form",
                "query": facturas_vigentes_vencidas_rango,
                "chartName": "facturasVigentes",
            },
        },
        ChartTypeChoices.FACTURAS_ORD: {
            BaseDateFilterFormChoices.DIA: {
                "class": dash_forms.ChartDateDayFilterForm,
                "name": "day_form",
                "query": facturas_ordenadas_fecha_cancelacion_dia,
                "chartName": "facturasOrdenadasFechaCancelacion",
            },
            BaseDateFilterFormChoices.MES: {
                "class": dash_forms.ChartDateMonthFilterForm,
                "name": "month_form",
                "query": facturas_ordenadas_fecha_cancelacion_mes,
                "chartName": "facturasOrdenadasFechaCancelacion",
            },
            BaseDateFilterFormChoices.INTERVALO: {
                "class": dash_forms.ChartDateRangeFilterForm,  # noqa: E501, E261
                "name": "range_form",
                "query": facturas_ordenadas_fecha_cancelacion_rango,
                "chartName": "facturasOrdenadasFechaCancelacion",
            },
        },
    }

    extra_context = {
        "datechoices": dash_forms.BaseDateFilterFormChoices,
        "chartIds": dash_forms.ChartTypeChoices,
    }

    def get(self, request, *args, **kwargs):
        # TODO: define default chart to render when no query params

        # No query params do normal get flow
        if not len(self.request.GET) > 0 and not self.request.htmx:
            return super().get(request, *args, **kwargs)

        f = self.form_class(data=self.request.GET)
        if not f.is_valid():
            return JsonResponse(
                data={
                    "form": f.errors,
                },
                status=400,
            )

        # Get the child form class and construct the form
        child_form_config = self.forms_config[
            f.cleaned_data.get("chart_type")
        ][f.cleaned_data.get("tipo")]

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

        if f.cleaned_data.get("chart_type") == ChartTypeChoices.FACTURAS_ORD:
            query_data = child_form_config["query"](actual_form)
            response = HttpResponse()
            response.write(
                """
                <table
                    id="facturasOrdenadasFechaCancelacion"
                    class="table w-full"
                >
                    <thead>
                        <tr>
                            <th class="w-1/2">Id Factura</th>
                            <th class="w-1/2">Tiempo de Cancelación</th>
                        </tr>
                    </thead>
                    <tbody>
            """
            )
            for data in query_data:
                response.write(
                    f"""
                    <tr>
                        <th>{data.id}</th>
                    """
                )
                for date in data.dates.all():
                    if date.status == Invoice.States.PAID:
                        response.write(
                            f"""
                            <td>{date.date.strftime("%d-%m-%Y")}</td>
                        """
                        )

            response.write(
                """
                        </tr>
                    </tbody>
                </table>
            """
            )
            return response

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
