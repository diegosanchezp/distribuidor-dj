"""
Forms of the dashboard
"""

from distribuidor_dj.apps.shipment.models import Shipment

from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class ShipmentsFilterForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = ["state"]


def exact_value_validator(value, message=None):
    """
    Checks that field value is equal to value
    """
    return validators.RegexValidator(regex=f"^({value})$", message=message)


class BaseDateFilterFormChoices(models.TextChoices):
    DIA = "dia", "Día"
    MES = "mes", "Mes"
    INTERVALO = "intervalo", "Intérvalo"


class ChartTypeChoices(models.TextChoices):
    ENVIOS = "despachadasPendientes", "Envios"
    CLIENTES = "clientesOrdenados", "Clientes"
    DESTINOS = "destinosOrdenados", "Destinos"
    FACTURAS_VG_VC = "vencidasVigentes", "Vencidas/vigentes"
    FACTURAS_ORD = "ordenadas", "Ordenadas"


class BaseDateFilterForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=BaseDateFilterFormChoices.choices, widget=forms.RadioSelect
    )
    chart_type = forms.ChoiceField(
        choices=ChartTypeChoices.choices,
        initial=ChartTypeChoices.ENVIOS,
    )


class DateRangeValidator:

    message = _("Fecha fuera del rango")

    def __init__(self, min_date, max_date, message=None, code=None):

        if not (min_date <= max_date):
            raise TypeError("min_date can be greater than max_date")

        self.min_date = min_date
        self.max_date = max_date

        if message is not None:
            self.message = message

        if code is not None:
            self.code = code

    def __call__(self, value):
        if not (self.min_date <= value <= self.max_date):
            raise ValidationError(
                self.message, code=self.code, params={"value": value}
            )


class ChartDateDayFilterForm(BaseDateFilterForm):
    dia = forms.DateField(
        initial=timezone.now(),
    )


class ChartDateMonthFilterForm(BaseDateFilterForm):
    month = forms.IntegerField(min_value=1, max_value=12)
    year = forms.ChoiceField(
        choices=[
            (f"{timezone.now().year -1}", f"{timezone.now().year -1}"),
            (f"{timezone.now().year}", f"{timezone.now().year}"),
        ],
    )


class ChartDateRangeFilterForm(BaseDateFilterForm):
    initial_date = forms.DateField()
    end_date = forms.DateField()

    def clean(self):
        cleaned_data = super().clean()
        initial_date = cleaned_data.get("initial_date")
        end_date = cleaned_data.get("end_date")

        if initial_date and end_date:
            if initial_date >= end_date:
                raise ValidationError("Fecha inicio mayor que fecha fin")


# TODO
class DakitiForm(forms.Form):
    card = forms.CharField()
    cvc = forms.CharField()
    expirationDate = forms.CharField()
