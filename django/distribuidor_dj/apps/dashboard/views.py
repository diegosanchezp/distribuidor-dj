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
    form_classes = {
        BaseDateFilterFormChoices.DIA: dash_forms.ChartDateDayFilterForm,
        BaseDateFilterFormChoices.MES: dash_forms.ChartDateMonthFilterForm,
        BaseDateFilterFormChoices.INTERVALO: dash_forms.ChartDateRangeFilterForm,  # noqa: E501, E261
    }

    extra_context = {"datechoices": dash_forms.BaseDateFilterFormChoices}

    def get(self, request, *args, **kwargs):
        # TODO: define default chart to render when no query params

        # No query params do normal get flow
        # if (not len(self.request.GET) > 0
        #         and not self.request.htmx):
        if not len(self.request.GET) > 0:
            return super().get(request, *args, **kwargs)

        f = self.form_class(data=self.request.GET)
        if not f.is_valid():
            return self.form_invalid(form=f)

        # Get the child form class and construct the form
        child_form_class = self.form_classes[f.cleaned_data.get("tipo")]
        actual_form = child_form_class(data=self.request.GET)

        if not actual_form.is_valid():
            return self.form_invalid(form=actual_form)

        # queryset = self.get_query()
        # Convert query to json

        # This should be an htmx response
        return self.render_to_response(self.get_context_data(form=actual_form))

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if "day_form" not in kwargs:
            ctx["day_form"] = dash_forms.ChartDateDayFilterForm()
        if "month_form" not in kwargs:
            ctx["month_form"] = dash_forms.ChartDateMonthFilterForm()
        if "range_form" not in kwargs:
            ctx["range_form"] = dash_forms.ChartDateRangeFilterForm()
        return ctx

    def get_query(self):
        pass

    # Querys
    def get_shipments_by_status(self, form):
        tipo = form.cleaned_data.get("tipo")
        # TODO refactor if's tipo, into dicts ?
        if tipo == BaseDateFilterFormChoices.DIA:
            # Order shipments
            # today_date = datetime.today()
            # q1 = ShipmentStatusDate.objects.filter(
            #     status=Shipment.States.RECIEVED,
            #     date__lte=today_date,
            # ).order_by("date")
            pass
