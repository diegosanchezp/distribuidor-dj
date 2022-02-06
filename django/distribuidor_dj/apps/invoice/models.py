import uuid
from enum import auto, unique

from distribuidor_dj.apps.state.models import StateMachineModel, StatusDate
from distribuidor_dj.utils import const
from distribuidor_dj.utils.enum import AutoName

from django.apps import apps
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


@unique
class InvoiceEvents(AutoName):
    ON_PAY = auto()


# Create your models here.
class Invoice(StateMachineModel):
    def __init__(self, *args, **kwargs):
        self.status_date_class = apps.get_model("invoice", "InvoiceStatusDate")
        super().__init__(*args, **kwargs)

    class States(models.TextChoices):
        """
        Invoice States enumeration
        """

        PAID = "PAID", _("Pagado")
        UNPAID = "UNPAID", _("No pagado")

    status_date_relattr = "invoice"

    machine = {
        States.UNPAID: {
            InvoiceEvents.ON_PAY: States.PAID,
        }
    }

    state = models.TextField(
        _("Estado"), choices=States.choices, default=States.UNPAID
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ammount = models.FloatField(validators=[MinValueValidator(0)])

    shipment = models.OneToOneField(
        "shipment.Shipment",
        verbose_name=_("Envio"),
        on_delete=models.CASCADE,
        related_name="invoice",
    )

    commerce = models.ForeignKey(
        "auth.User",
        limit_choices_to={"groups__name": const.COMMERCE_GROUP_NAME},
        verbose_name=_("Cliente comercio"),
        # delete shipment if customer deleted
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.commerce} {self.state}"


class InvoiceStatusDate(StatusDate):
    """
    Date by status of an invoice
    """

    status = models.TextField(
        _("Estado"),
        choices=Invoice.States.choices,
        default=Invoice.States.UNPAID,
    )

    invoice = models.ForeignKey(
        "Invoice",
        related_name="dates",
        # Delete this if invoice is deleted
        on_delete=models.CASCADE,
    )
