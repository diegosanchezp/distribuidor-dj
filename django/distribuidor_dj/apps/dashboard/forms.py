"""
Forms of the dashboard
"""

from distribuidor_dj.apps.shipment.models import Shipment, ShipmentStatusDate

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


class BaseDateFilterForm(forms.Form):
    tipo = forms.ChoiceField(
        choices=BaseDateFilterFormChoices.choices, widget=forms.RadioSelect
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
    dia = forms.DateField()
    # the format that html5 date input accepts
    date_format = "%Y-%m-%d"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dia_field = self.fields["dia"]  # alias
        # Get valid dates
        today_date = timezone.now()

        dates = ShipmentStatusDate.objects.filter(
            status=Shipment.States.CREATED,
            date__lte=today_date,
        ).order_by("date")

        self.min_date = dates.first().date.date()
        self.max_date = dates.last().date.date()

        # Set validators
        dia_field.validators = [
            DateRangeValidator(
                min_date=self.min_date,
                max_date=self.max_date,
            )
        ]

        max_date = self.max_date.strftime(self.date_format)
        dia_field.widget.attrs.update(
            {
                "min": self.min_date.strftime(self.date_format),
                "max": max_date,
            }
        )

        dia_field.initial = max_date


class ChartDateMonthFilterForm(BaseDateFilterForm):
    month = forms.IntegerField()
    pass


class ChartDateRangeFilterForm(BaseDateFilterForm):
    inital_date = forms.DateField(validators=[])
    end_date = forms.DateField(validators=[])
