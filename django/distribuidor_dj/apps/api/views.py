from typing import OrderedDict

from distribuidor_dj.apps.shipment.models import (
    Address,
    Product,
    ProductQuantity,
    Shipment,
    ShipmentStatusDate,
)
from distribuidor_dj.utils import const
from rest_framework import serializers, viewsets

from django.contrib.auth import get_user_model


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
    # Probably for later
    # state = serializers.SlugRelatedField(
    #     slug_field="state",
    #     queryset=CountryStates.objects.all(),
    #     many=False,
    # )
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
    initial_address = AddressSerializer(required=True)
    target_address = AddressSerializer(required=True)

    class Meta:
        model = Shipment
        fields = [
            "id",
            "productquantity_set",
            "target_address",
            "initial_address",
            "commerce",
            "state",
        ]
        read_only_fields = ["id", "state"]

    def create(self, validated_data):
        products_dict = validated_data.pop("productquantity_set")
        # Create Addresses
        initial_address, _ = Address.objects.get_or_create(
            **validated_data.pop("initial_address")
        )
        target_address, _ = Address.objects.get_or_create(
            **validated_data.pop("target_address")
        )

        shipment = Shipment.objects.create(
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

        return shipment


# Create your views here.
class ShipmentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    serializer_class = ShipmentSerializer
    queryset = Shipment.objects.all()


"""
{
    target_address: {
        state: "",
        city: "",
    },
    initial_address: {
        state: "",
        city: "",
    },
    products: [
        {
            name: "PlayStation 5",
            quantity: "1",
        },
    ],
    commerce: "commerce_username_from_our_platform",
}
"""
