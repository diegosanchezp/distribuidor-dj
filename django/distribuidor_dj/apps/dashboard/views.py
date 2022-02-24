"""
Dashboard views
"""
from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment

from django.db.models.query import QuerySet
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


class ReportesView(AdminDashboardPassessTest, FormView):
    template_name = "dashboard/reportes.html"
    form_class = dash_forms.BaseDateFilterForm  # Root form class

    def get(self, request, *args, **kwargs):

        if len(self.request.GET) > 0:
            f = self.form_class(data=self.request.GET)
            # breakpoint()
            if f.is_valid():
                actual_form_class = self.get_child_form(f)
                actual_form = actual_form_class(data=self.request.GET)
                if actual_form.is_valid():
                    self.make_querys()
                    self.render_to_response(
                        self.get_context_data(form=actual_form)
                    )
            else:
                return self.form_invalid(form=f)
        return super().get(request, *args, **kwargs)

    # TODO refactor if's tipo, into dicts
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if "day_form" not in kwargs:
            ctx["day_form"] = dash_forms.ChartDateDayFilterForm()
        if "month_form" not in kwargs:
            ctx["month_form"] = dash_forms.ChartDateMonthFilterForm()
        if "range_form" not in kwargs:
            ctx["range_form"] = dash_forms.ChartDateRangeFilterForm()
        return ctx

    def make_querys(self):
        pass

    def get_child_form(self, parent_form):
        tipo = parent_form.cleaned_data.get("tipo")
        if tipo == BaseDateFilterFormChoices.DIA:
            return dash_forms.ChartDateDayFilterForm
        elif tipo == BaseDateFilterFormChoices.MES:
            return dash_forms.ChartDateMonthFilterForm
        elif tipo == BaseDateFilterFormChoices.INTERVALO:
            return dash_forms.ChartDateRangeFilterForm

    # Querys
    def get_shipments_by_status(self, tipo: str):

        if tipo == BaseDateFilterFormChoices.DIA:
            Shipment.objects.filter(
                status=Shipment.States.RECIEVED, dates__date__range=[]
            )
