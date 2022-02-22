"""
Forms of the dashboard
"""
from distribuidor_dj.apps.shipment.models import Shipment

from django.forms import ModelForm


class ShipmentsFilterForm(ModelForm):
    class Meta:
        model = Shipment
        fields = ["state"]
