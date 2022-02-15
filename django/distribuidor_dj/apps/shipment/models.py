import uuid
from datetime import datetime
from enum import auto, unique
from typing import Union

from distribuidor_dj.apps.state.models import StateMachineModel, StatusDate
from distribuidor_dj.utils import const
from distribuidor_dj.utils.enum import AutoName

from django.apps import apps
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


@unique
class ShipmentEvents(AutoName):
    ON_SEND = auto()
    ON_RECIEVE = auto()


class Shipment(StateMachineModel):
    def __init__(self, *args, **kwargs):
        self.status_date_class = apps.get_model(
            "shipment", "ShipmentStatusDate"
        )
        super().__init__(*args, **kwargs)

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

    class Events(models.TextChoices):
        """
        Shipment States enumeration
        """

        ON_SEND = "ON_SEND", _("Enviar")
        ON_RECIEVE = "ON_RECIEVE", _("Recibir")

    status_date_relattr = "shipment"

    default_address_q = Q(
        state__name="Distrito Capital",
        city="Caracas",
        street="Calle New York",
        zipcode=1073,
    )
    machine = {
        States.SENDED: {
            Events.ON_RECIEVE: States.RECIEVED,
        },
        States.CREATED: {
            Events.ON_SEND: States.SENDED,
        },
    }

    state = models.TextField(
        _("Estatus"),
        choices=States.choices,
        default=States.CREATED,
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    products = models.ManyToManyField(
        "Product",
        verbose_name=_("Productos"),
        through="ProductQuantity",
        through_fields=("shipment", "product"),
    )

    target_address = models.ForeignKey(
        "Address",
        null=True,
        verbose_name=_("Dirección destino"),
        # set to null this column if address deleted
        on_delete=models.SET_NULL,
        related_name="shipment_target_addresses",
        limit_choices_to=~default_address_q,
    )

    initial_address = models.ForeignKey(
        "Address",
        verbose_name=("Dirección inicial"),
        null=True,
        on_delete=models.SET_NULL,
        related_name="shipment_initial_addresses",
        limit_choices_to=default_address_q,
    )

    customer = models.ForeignKey(
        "auth.User",
        verbose_name=_("Cliente del comercio"),
        limit_choices_to={"groups__name": const.CLIENT_GROUP_NAME},
        # delete shipment if customer deleted
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    commerce = models.ForeignKey(
        "auth.User",
        verbose_name=_("Usuario comercio"),
        limit_choices_to={"groups__name": const.COMMERCE_GROUP_NAME},
        related_name="shipments",  # envios
        # delete shipment if customer deleted
        on_delete=models.CASCADE,
    )

    # TODO: field for distance between target and initial address

    def __str__(self) -> str:
        return f"{self.state} {self.commerce.username}"

    def get_current_status_date(self) -> Union[datetime, None]:
        """
        Get the the date of the current status
        """
        try:
            date: ShipmentStatusDate = self.dates.get(status=self.state)
            return date.date
        except ShipmentStatusDate.DoesNotExist:
            return None


class ShipmentStatusDate(StatusDate):
    """
    Shipment status and date
    """

    status = models.TextField(
        _("Estatus"),
        choices=Shipment.States.choices,
        default=Shipment.States.SENDED,
    )

    shipment = models.ForeignKey(
        "Shipment",
        related_name="dates",
        # Delete this if shipment is deleted
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.date} {self.status}"


class ProductManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)


class Product(models.Model):
    name = models.TextField(_("Nombre"), unique=True)

    objects = ProductManager()

    def natural_key(self):
        return (self.name,)

    def __str__(self) -> str:
        desc = (self.name[:30] + "...") if len(self.name) > 33 else self.name
        return f"{desc}"


class ProductQuantity(models.Model):
    """
    Many to many between product and shipment
    """

    product = models.ForeignKey(
        "Product",
        verbose_name=_("Producto"),
        on_delete=models.CASCADE,
    )

    shipment = models.ForeignKey(
        "Shipment",
        verbose_name=_("Envio"),
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField(
        _("Cantidad"), validators=[MinValueValidator(1)]
    )


class Address(models.Model):
    state = models.ForeignKey(
        "AddressState",
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("Estado"),
    )
    city = models.TextField(_("Ciudad"))
    street = models.TextField(_("Calle"))
    zipcode = models.TextField(
        _("Codigo Zip"),
        blank=True,
    )  # optional

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        unique_together = [["state", "city", "street"]]

    def __str__(self) -> str:
        return f"{self.state}, {self.city}, {self.street}"


class AddressStateManager(models.Manager):
    use_in_migrations = True

    def get_by_natural_key(self, name, price):
        return self.get(name=name, price=price)


class AddressState(models.Model):
    name = models.TextField(_("Estado"), unique=True)
    price = models.FloatField(_("Precio"), validators=[MinValueValidator(0)])
    objects = AddressStateManager()

    def natural_key(self):
        return (self.name, self.price)

    def __str__(self) -> str:
        return f"{self.name}"
