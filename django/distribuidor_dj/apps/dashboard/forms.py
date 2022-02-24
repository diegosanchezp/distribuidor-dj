"""
Forms of the dashboard
"""
from distribuidor_dj.apps.shipment.models import Shipment

from django import forms
from django.core import validators
from django.db import models


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


class BaseDateFilterForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=BaseDateFilterFormChoices.choices, widget=forms.RadioSelect
    )


class ChartDateDayFilterForm(BaseDateFilterForm):
    date = forms.DateField(validators=[])


class ChartDateMonthFilterForm(BaseDateFilterForm):
    month = forms.IntegerField()
    pass


class ChartDateRangeFilterForm(BaseDateFilterForm):
    inital_date = forms.DateField(validators=[])
    end_date = forms.DateField(validators=[])
