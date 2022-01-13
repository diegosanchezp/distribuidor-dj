from enum import auto, unique

from distribuidor_dj.apps.state.models import StateMachineModel, StatusDate
from distribuidor_dj.utils.enum import AutoName

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class InvoiceStatusDate(StatusDate):
    invoice = models.ForeignKey(
        "Invoice",
        related_name="dates",
        # Delete this if invoice is deleted
        on_delete=models.CASCADE,
    )


@unique
class InvoiceEvents(AutoName):
    ON_PAY = auto()


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

    state = models.TextField(_("Estado"), choices=States.choices)

    ammount = models.FloatField(validators=[MinValueValidator(0)])
