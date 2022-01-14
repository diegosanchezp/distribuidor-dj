from enum import auto, unique

from distribuidor_dj.apps.state.models import StateMachineModel, StatusDate
from distribuidor_dj.utils.enum import AutoName

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


@unique
class InvoiceEvents(AutoName):
    ON_PAY = auto()


# Create your models here.
class Invoice(StateMachineModel):
    class States(models.TextChoices):
        """
        Invoice States enumeration
        """

        PAID = "PAID", _("Pagado")
        UNPAID = "UNPAID", _("No pagado")

    machine = {
        States.UNPAID: {
            InvoiceEvents.ON_PAY: States.PAID,
        }
    }

    state = models.TextField(
        _("Estado"), choices=States.choices, default=States.UNPAID
    )

    ammount = models.FloatField(validators=[MinValueValidator(0)])

    shipment = models.OneToOneField(
        "invoice.Invoice",
        verbose_name=_("Envio"),
        on_delete=models.CASCADE,
        related_name="invoice",
    )

    # TODO: limit to groups
    commerce = models.ForeignKey(
        "customer.Customer",
        verbose_name=_("Cliente comercio"),
        # delete shipment if customer deleted
        on_delete=models.CASCADE,
    )


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
