# Generated by Django 4.0 on 2022-02-06 15:53

import uuid

import distribuidor_dj.apps.shipment.models

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
            fields=[
                ("city", models.TextField(verbose_name="Ciudad")),
                ("street", models.TextField(verbose_name="Calle")),
                (
                    "zipcode",
                    models.TextField(blank=True, verbose_name="Codigo Zip"),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AddressState",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(unique=True, verbose_name="Estado")),
                (
                    "price",
                    models.FloatField(
                        validators=[
                            django.core.validators.MinValueValidator(0)
                        ],
                        verbose_name="Precio",
                    ),
                ),
            ],
            managers=[
                (
                    "objects",
                    distribuidor_dj.apps.shipment.models.AddressStateManager(),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(unique=True, verbose_name="Nombre")),
            ],
            managers=[
                (
                    "objects",
                    distribuidor_dj.apps.shipment.models.ProductManager(),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductQuantity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "quantity",
                    models.PositiveIntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1)
                        ],
                        verbose_name="Cantidad",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="shipment.product",
                        verbose_name="Producto",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Shipment",
            fields=[
                (
                    "state",
                    models.TextField(
                        choices=[
                            ("SENDED", "Enviado"),
                            ("CREATED", "Creado"),
                            ("RECIEVED", "Recibido"),
                        ],
                        default="CREATED",
                        verbose_name="Estatus",
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "commerce",
                    models.ForeignKey(
                        limit_choices_to={"groups__name": "comercio"},
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shipments",
                        to="auth.user",
                        verbose_name="Usuario comercio",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"groups__name": "cliente"},
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="auth.user",
                        verbose_name="Cliente del comercio",
                    ),
                ),
                (
                    "initial_address",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            ("city", "Caracas"),
                            ("state__name", "Distrito Capital"),
                            ("street", "Calle New York"),
                            ("zipcode", 1073),
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="shipment_initial_addresses",
                        to="shipment.address",
                        verbose_name="Direcci??n inicial",
                    ),
                ),
                (
                    "products",
                    models.ManyToManyField(
                        through="shipment.ProductQuantity",
                        to="shipment.Product",
                        verbose_name="Productos",
                    ),
                ),
                (
                    "target_address",
                    models.ForeignKey(
                        limit_choices_to=models.Q(
                            ("city", "Caracas"),
                            ("state__name", "Distrito Capital"),
                            ("street", "Calle New York"),
                            ("zipcode", 1073),
                            _negated=True,
                        ),
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="shipment_target_addresses",
                        to="shipment.address",
                        verbose_name="Direcci??n destino",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ShipmentStatusDate",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Fecha"
                    ),
                ),
                (
                    "status",
                    models.TextField(
                        choices=[
                            ("SENDED", "Enviado"),
                            ("CREATED", "Creado"),
                            ("RECIEVED", "Recibido"),
                        ],
                        default="SENDED",
                        verbose_name="Estatus",
                    ),
                ),
                (
                    "shipment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dates",
                        to="shipment.shipment",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="productquantity",
            name="shipment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="shipment.shipment",
                verbose_name="Envio",
            ),
        ),
        migrations.AddField(
            model_name="address",
            name="state",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="addresses",
                to="shipment.addressstate",
                verbose_name="Estado",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="address",
            unique_together={("state", "city", "street")},
        ),
    ]
