import uuid

from distribuidor_dj.apps.state.models import StateMachineModel, StatusDate
from distribuidor_dj.utils import const

from django.apps import apps
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        OVERDUE = "OVERDUE", _("Vencida")
        UNPAID = "UNPAID", _("No pagado")

    class Events(models.TextChoices):
        """
        Invoice Events enumeration
        """

        ON_PAY = "ON_PAY", _("Pagar")
        ON_OVERDUE = "ON_OVERDUE", _("Marcar como vencida")

    status_date_relattr = "invoice"

    machine = {
        States.UNPAID: {
            Events.ON_PAY: States.PAID,
            Events.ON_OVERDUE: States.OVERDUE,
        },
        States.OVERDUE: {
            Events.ON_PAY: States.PAID,
        },
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
