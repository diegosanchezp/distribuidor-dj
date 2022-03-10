"""
Forms of the dashboard
"""
from distribuidor_dj.apps.shipment.models import Shipment

from django import forms
from django.forms import ModelForm


class ShipmentsFilterForm(ModelForm):
    class Meta:
        model = Shipment
        fields = ["state"]


# TODO
class DakitiForm(forms.Form):
    card = forms.CharField()
    cvc = forms.CharField()
    expirationDate = forms.CharField()
