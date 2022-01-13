from enum import auto, unique

from distribuidor_dj.apps.state.models import StateMachineModel, StatusDate
from distribuidor_dj.utils.enum import AutoName

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


@unique
class ShipmentEvents(AutoName):
    ON_SEND = auto()
    ON_RECIEVE = auto()


class ShipmentStatusDate(StatusDate):
    """
    Shipment status and date
    """

    shipment = models.ForeignKey(
        "Shipment",
        related_name="dates",
        # Delete this if shipment is deleted
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.date} {self.status}"


class Shipment(StateMachineModel):
    class States(models.TextChoices):
        """
        Shipment States enumeration
        """

        SENDED = "SENDED", _("Enviado")  # Shipment request is sent
        # by warehouse

        CREATED = "CREATED", _("Creado")  # Inital state,
        # shipment hasn't been sent
        # by warehouse

        RECIEVED = "RECIEVED", _("Recibido")  # The shipment product has
        # reached its target
        # Final state

    machine = {
        States.SENDED: {
            ShipmentEvents.ON_RECIEVE: States.RECIEVED,
        },
        States.CREATED: {
            ShipmentEvents.ON_SEND: States.SENDED,
        },
    }

    state = models.TextField(
        _("Estatus"),
        choices=States.choices,
        default=States.CREATED,
    )

    products = models.ManyToManyField("Product")

    target_address = models.OneToOneField(
        "Address",
        null=True,
        on_delete=models.SET_NULL,
        related_name="shipment_target_address",
    )

    initial_address = models.OneToOneField(
        "Address",
        null=True,
        on_delete=models.SET_NULL,
        related_name="shipment_initial_address",
    )
    # TODO: field for distance between target and initial address

    def __str__(self) -> str:
        return f"{self.state}"


class Product(StateMachineModel):
    description = models.TextField(_("Descripción"))
    quantity = models.PositiveIntegerField(
        _("Cantidad"), validators=[MinValueValidator(1)]
    )

    def __str__(self) -> str:
        desc = (
            (self.description[:30] + "...")
            if len(self.description) > 33
            else self.description
        )
        return f"{desc} {self.quantity}"


class Address(models.Model):
    state = models.TextField(_("Estado"))
    city = models.TextField(_("Ciudad"))
    street = models.TextField(_("Calle"))
    zipcode = models.TextField(
        _("Codigo Zip"),
        blank=True,
    )  # optional

    def __str__(self) -> str:
        return f"{self.state} {self.city} {self.street}"
