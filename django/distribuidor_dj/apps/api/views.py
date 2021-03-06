import json
import logging
from typing import OrderedDict

from cryptography.fernet import Fernet
from distribuidor_dj.apps.invoice.models import Invoice, InvoiceStatusDate
from distribuidor_dj.apps.shipment.models import (
    Address,
    AddressState,
    Product,
    ProductQuantity,
    Shipment,
    ShipmentStatusDate,
)
from distribuidor_dj.utils import const
from rest_framework import serializers, status, viewsets
from rest_framework.parsers import BaseParser
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class PlainTextParser(BaseParser):
    """
    Plain text parser.
    https://www.django-rest-framework.org/api-guide/parsers/
    """

    media_type = "text/plain"

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Simply return a string representing the body of the request.
        """

        logger.debug("Media type %s", media_type)
        return stream.read()


class PaymentsAPI(APIView):
    """
    This endpoint can only be executed in production
    https://bank.vittorioadesso.com/payways/docs
    """

    parser_classes = [PlainTextParser]

    def post(self, request, format=None):
        private_key: str = settings.PGT_PRIVATE_KEY
        secret = Fernet(key=private_key.encode(encoding="utf8"))
        message_str = secret.decrypt(request.data).decode("utf8")
        message: dict[str, str] = json.loads(message_str)

        if message["status"] == "DENIED":
            # return error response
            return Response(message, status=status.HTTP_409_CONFLICT)

        if message["status"] == "APPROVED":
            # Marcar el invoice como pagado
            invoice = Invoice.objects.get(id=message["order"])
            status_date = invoice.transition_set_date(Invoice.Events.ON_PAY)
            status_date.save()
            invoice.save()

            logger.debug(msg="Success, bank contacted")
            logger.debug("Decripted info %s", message_str)
            return Response(status=status.HTTP_200_OK)

        pass


class ProductQuantitySerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    def to_representation(self, instance: ProductQuantity):
        ret = OrderedDict()
        ret["name"] = instance.product.name
        ret["quantity"] = instance.quantity
        return ret

    class Meta:
        model = ProductQuantity
        fields = ["quantity", "name"]


class AddressSerializer(serializers.ModelSerializer):
    state = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AddressState.objects.all(),
        many=False,
    )

    class Meta:
        model = Address
        # We don't want to enforce UniqueTogetherValidator
        validators = []
        exclude = ["id"]


class ShipmentSerializer(serializers.ModelSerializer):
    productquantity_set = ProductQuantitySerializer(
        many=True, read_only=False, allow_empty=False
    )
    commerce = serializers.SlugRelatedField(
        slug_field="username",
        queryset=get_user_model().objects.filter(
            groups__name=const.COMMERCE_GROUP_NAME
        ),
        many=False,
    )
    initial_address = AddressSerializer(required=False, read_only=True)
    target_address = AddressSerializer(required=True)
    price = serializers.FloatField(read_only=True, min_value=0)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "productquantity_set",
            "target_address",
            "initial_address",
            "commerce",
            "state",
            "price",
        ]
        read_only_fields = [
            "id",
            "state",
            "price",
        ]

    def create(self, validated_data):
        products_dict = validated_data.pop("productquantity_set")

        initial_address = Address.objects.get(Shipment.default_address_q)

        # Create Addresses
        target_address, _ = Address.objects.get_or_create(
            **validated_data.pop("target_address")
        )

        shipment: "Shipment" = Shipment.objects.create(
            initial_address=initial_address,
            target_address=target_address,
            **validated_data
        )

        # Set creation status date
        ShipmentStatusDate.objects.create(
            shipment=shipment, status=shipment.state
        )

        pqs = []
        for product_dict in products_dict:
            product, _ = Product.objects.get_or_create(
                name=product_dict.get("name")
            )

            pqs.append(
                ProductQuantity(
                    product=product,
                    shipment=shipment,
                    quantity=product_dict.get("quantity"),
                )
            )

        ProductQuantity.objects.bulk_create(pqs)

        # Create invoice
        invoice = Invoice.objects.create(
            shipment=shipment,
            commerce=validated_data["commerce"],
            ammount=target_address.state.price,
        )

        InvoiceStatusDate.objects.create(
            invoice=invoice,
            status=invoice.state,
        )

        return shipment

    def to_representation(self, shipment: Shipment):
        ret = super().to_representation(shipment)
        ret["price"] = shipment.target_address.state.price
        return ret


# Create your views here.
class ShipmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing shipment instances.
    """

    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()


class AddressStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressState
        exclude = ["id"]


class AddressStateViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing address state instances.
    """

    serializer_class = AddressStateSerializer
    queryset = AddressState.objects.all()
