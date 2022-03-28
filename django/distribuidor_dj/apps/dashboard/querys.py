"""
Querys para los filtros del dashboard.
"""
from typing import Tuple

from distribuidor_dj.apps.invoice.models import Invoice, InvoiceStatusDate
from distribuidor_dj.apps.shipment.models import AddressState, Shipment
from distribuidor_dj.utils import const

from django.contrib.auth.models import User
from django.db.models import DurationField, F
from django.db.models.expressions import ExpressionWrapper, OuterRef, Subquery

from .forms import BaseDateFilterFormChoices


class BaseDashQuery:
    field_lookups: list[Tuple[str, str]]

    date_field_lookups = {
        BaseDateFilterFormChoices.DIA: [("dates__date__date", "dia")],
        BaseDateFilterFormChoices.MES: [
            ("dates__date__year", "year"),
            ("dates__date__month", "month"),
        ],
        BaseDateFilterFormChoices.INTERVALO: [
            ("dates__date__range", ["initial_date", "end_date"]),
        ],
    }

    def __init__(self, date_filter: "BaseDateFilterFormChoices") -> None:
        self.field_lookups = self.date_field_lookups[date_filter]

    def __call__(self, **kwargs):
        # field_value_lookups has to be reset here,
        # not in __init__ because it's populated by
        # the previous call to this method
        self.field_value_lookups = {}
        for field_lookup, field_value in self.field_lookups:

            if isinstance(field_value, list):
                self.field_value_lookups[field_lookup] = [
                    kwargs[field_value[0]],
                    kwargs[field_value[1]],
                ]
            else:
                self.field_value_lookups[field_lookup] = kwargs[field_value]


# Querys
class SolicitudesDespachadasPendientes(BaseDashQuery):
    def __call__(self, **kwargs):
        super().__call__(**kwargs)
        # Obtener numero solictudes pendientes por despachar
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            **self.field_value_lookups,
        ).count()

        # Obtener numero solictudes despachadas
        # en el dia especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            **self.field_value_lookups,
        ).count()

        # Hacer calculos de porcentajes
        # 1. Despachadas
        p_pendientes = n_pendientes
        p_despachadas = n_despachadas

        # Retornar data ajustada a chart.js
        return (
            p_pendientes,
            p_despachadas,
        )


class FacturasVigentesVencidas(BaseDashQuery):
    def __call__(self, **kwargs):
        super().__call__(**kwargs)

        # Obtener numero facturas vigentes pendientes por cobrar
        # en el dia especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            **self.field_value_lookups,
        ).count()

        # Obtener numero facturas vencidas pendientes por cobrar
        # en el dia especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.OVERDUE,
            dates__status=Invoice.States.OVERDUE,
            # casts the datetime as date
            **self.field_value_lookups,
        ).count()

        # Hacer calculos de porcentajes
        # 1. Vigentes
        p_vigentes = n_vigentes
        p_vencidas = n_vencidas

        # Retornar data ajustada a chart.js
        return (
            p_vigentes,
            p_vencidas,
        )


class FacturasOrdenadasTiempoCancelacion(BaseDashQuery):
    def __call__(self, **kwargs):
        super().__call__(**kwargs)
        paidSub = InvoiceStatusDate.objects.filter(
            invoice=OuterRef("pk"), status=Invoice.States.PAID
        )
        unpaidSub = InvoiceStatusDate.objects.filter(
            invoice=OuterRef("pk"), status=Invoice.States.UNPAID
        )

        ordenadas = (
            Invoice.objects.filter(
                state=Invoice.States.PAID,
                dates__status=Invoice.States.PAID,
                **self.field_value_lookups,
            )
            .annotate(
                date_paid=Subquery(paidSub.values("date")[:1]),
                date_init=Subquery(unpaidSub.values("date")[:1]),
            )
            .annotate(
                tiempo_cancelacion=ExpressionWrapper(
                    F("date_paid") - F("date_init"),
                    output_field=DurationField(),
                )
            )
            .order_by("tiempo_cancelacion")
        )
        return ordenadas


class DestinosOrdenadosSolicitudesRealizadas(BaseDashQuery):
    def __call__(self, **kwargs):
        super().__call__(**kwargs)
        destinos = AddressState.objects.all()
        totales_destinos = []

        for destino in destinos:
            total_destino = Shipment.objects.filter(
                target_address__state=destino.id,
                **self.field_value_lookups,
            ).count()
            totales_destinos.append(total_destino)

            return {
                "destinos": list(destinos.values()),
                "totales_destinos": totales_destinos,
            }


class ClientesOrdenadosSolicitudesRealizadas(BaseDashQuery):
    def __call__(self, **kwargs):
        super().__call__(**kwargs)

        clientes = list(
            User.objects.filter(groups__name=const.COMMERCE_GROUP_NAME).values(
                "id", "username"
            )
        )

        totales_clientes = []

        for cliente in clientes:
            total_cliente = Shipment.objects.filter(
                commerce=cliente["id"],
                **self.field_value_lookups,
            ).count()
            totales_clientes.append(total_cliente)

        return {"clientes": clientes, "totales_clientes": totales_clientes}


# Query Alias
solicitudes_despachadas_pendientes_dia = SolicitudesDespachadasPendientes(
    date_filter=BaseDateFilterFormChoices.DIA
)

solicitudes_despachadas_pendientes_mes = SolicitudesDespachadasPendientes(
    date_filter=BaseDateFilterFormChoices.MES
)

solicitudes_despachadas_pendientes_rango = SolicitudesDespachadasPendientes(
    date_filter=BaseDateFilterFormChoices.INTERVALO
)

facturas_vigentes_vencidas_dia = FacturasVigentesVencidas(
    date_filter=BaseDateFilterFormChoices.DIA
)

facturas_vigentes_vencidas_mes = FacturasVigentesVencidas(
    date_filter=BaseDateFilterFormChoices.MES
)

facturas_vigentes_vencidas_rango = FacturasVigentesVencidas(
    date_filter=BaseDateFilterFormChoices.INTERVALO
)

facturas_ordenadas_tiempo_cancelacion_dia = FacturasOrdenadasTiempoCancelacion(
    date_filter=BaseDateFilterFormChoices.DIA
)

facturas_ordenadas_tiempo_cancelacion_mes = FacturasOrdenadasTiempoCancelacion(
    date_filter=BaseDateFilterFormChoices.MES
)

facturas_ordenadas_tiempo_cancelacion_rango = (
    FacturasOrdenadasTiempoCancelacion(
        date_filter=BaseDateFilterFormChoices.INTERVALO
    )
)

destinos_ordenados_solicitudes_realizadas_dia = (
    DestinosOrdenadosSolicitudesRealizadas(
        date_filter=BaseDateFilterFormChoices.DIA
    )
)

destinos_ordenados_solicitudes_realizadas_mes = (
    DestinosOrdenadosSolicitudesRealizadas(
        date_filter=BaseDateFilterFormChoices.MES
    )
)

destinos_ordenados_solicitudes_realizadas_rango = (
    DestinosOrdenadosSolicitudesRealizadas(
        date_filter=BaseDateFilterFormChoices.INTERVALO
    )
)

clientes_ordenados_solicitudes_realizadas_dia = (
    ClientesOrdenadosSolicitudesRealizadas(
        date_filter=BaseDateFilterFormChoices.DIA
    )
)

clientes_ordenados_solicitudes_realizadas_mes = (
    ClientesOrdenadosSolicitudesRealizadas(
        date_filter=BaseDateFilterFormChoices.MES
    )
)

clientes_ordenados_solicitudes_realizadas_rango = (
    ClientesOrdenadosSolicitudesRealizadas(
        date_filter=BaseDateFilterFormChoices.INTERVALO
    )
)
