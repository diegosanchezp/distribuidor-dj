"""
Querys para los filtros del dashboard.
"""
from datetime import timedelta

from distribuidor_dj.apps.invoice.models import Invoice
from distribuidor_dj.apps.shipment.models import Shipment

from django.utils import timezone


# Querys
def solicitudes_despachadas_pendientes_dia(form):
    # Obtener fecha especificada por defecto
    # si el formulario no esta rellenado
    fecha_especificada = form.fields["dia"].initial
    if form.is_valid():
        fecha_especificada = form.cleaned_data["dia"]

        # Obtener numero solictudes pendientes por despachar
        # en el dia especificado de tiempo
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            dates__date__date=fecha_especificada,
        ).count()

        # Obtener numero solictudes despachadas
        # en el dia especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            dates__date__date=fecha_especificada,
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


def solicitudes_despachadas_pendientes_mes(form):
    if form.is_valid():
        month = form.cleaned_data["month"]
        # Obtener numero solictudes pendientes por despachar
        # en el mes/añi especificado de tiempo
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            dates__date__month=month,
            dates__date__year=timezone.now().year,
        ).count()

        # Obtener numero solictudes despachadas
        # en el mes/año especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            dates__date__month=month,
            dates__date__year=timezone.now().year,
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


def solicitudes_despachadas_pendientes_rango(form):
    if form.is_valid():
        initial_date = form.cleaned_data["initial_date"]
        end_date = form.cleaned_data["end_date"]

        # Obtener numero solictudes pendientes por despachar
        # en el rango especificado de tiempo
        n_pendientes = Shipment.objects.filter(
            state=Shipment.States.CREATED,
            dates__status=Shipment.States.CREATED,
            # casts the datetime as date
            dates__date__range=[initial_date, end_date],
        ).count()

        # Obtener numero solictudes despachadas
        # en el rango especificado de tiempo
        n_despachadas = Shipment.objects.filter(
            state=Shipment.States.SENDED,
            dates__status=Shipment.States.SENDED,
            # casts the datetime as date
            dates__date__range=[initial_date, end_date],
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


def facturas_vigentes_vencidas_dia(form):
    # Obtener fecha especificada por defecto
    # si el formulario no esta rellenado
    fecha_especificada = form.fields["dia"].initial
    if form.is_valid():
        fecha_especificada = form.cleaned_data["dia"]

        # Obtener numero facturas vigentes pendientes por cobrar
        # en el dia especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__date__range=[timezone.now(), fecha_especificada],
        ).count()

        # Obtener numero facturas vencidas pendientes por cobrar
        # en el dia especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__date__range=[fecha_especificada, timezone.now()],
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


def facturas_vigentes_vencidas_mes(form):
    if form.is_valid():
        month = form.cleaned_data["month"]
        # Obtener numero solictudes pendientes por despachar
        # en el mes/año especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__month__gte=month,
            dates__date__year__gte=timezone.now().year - 1,
            dates__date__date__gte=timezone.now(),
        ).count()

        # Obtener numero solictudes despachadas
        # en el mes/año especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__month=month,
            dates__date__year=timezone.now().year - 1,
            dates__date__date__lt=timezone.now(),
        ).count()

        # Hacer calculos de porcentajes
        # 1. Despachadas
        p_vigentes = n_vigentes
        p_vencidas = n_vencidas

        # Retornar data ajustada a chart.js
        return (p_vigentes, p_vencidas)


def facturas_vigentes_vencidas_rango(form):
    if form.is_valid():
        initial_date = form.cleaned_data["initial_date"]
        end_date = form.cleaned_data["end_date"]
        # Obtener numero solictudes pendientes por despachar
        # en el mes/año especificado de tiempo
        n_vigentes = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__range=[timezone.now(), end_date],
        ).count()

        # Obtener numero solictudes despachadas
        # en el mes/año especificado de tiempo
        n_vencidas = Invoice.objects.filter(
            state=Invoice.States.UNPAID,
            dates__status=Invoice.States.UNPAID,
            # casts the datetime as date
            dates__date__range=[
                initial_date,
                timezone.now() - timedelta(days=1),
            ],
        ).count()

        # Hacer calculos de porcentajes
        # 1. Despachadas
        p_vigentes = n_vigentes
        p_vencidas = n_vencidas

        # Retornar data ajustada a chart.js
        return (p_vigentes, p_vencidas)


def facturas_ordenadas_fecha_cancelacion_dia(form):
    if form.is_valid():
        fecha_especificada = form.cleaned_data["dia"]
        ordenadas = Invoice.objects.filter(
            state=Invoice.States.PAID,
            dates__status=Invoice.States.PAID,
            dates__date__date=fecha_especificada,
        ).order_by("dates")

        ordenadas = list(ordenadas)

        return ordenadas


def facturas_ordenadas_fecha_cancelacion_mes(form):
    if form.is_valid():
        month = form.cleaned_data["month"]
        ordenadas = Invoice.objects.filter(
            state=Invoice.States.PAID,
            dates__status=Invoice.States.PAID,
            dates__date__month=month,
            dates__date__year=timezone.now().year,
        ).order_by("dates")

        ordenadas = list(ordenadas)

        return ordenadas


def facturas_ordenadas_fecha_cancelacion_rango(form):
    if form.is_valid():
        initial_date = form.cleaned_data["initial_date"]
        end_date = form.cleaned_data["end_date"]
        ordenadas = Invoice.objects.filter(
            state=Invoice.States.PAID,
            dates__status=Invoice.States.PAID,
            dates__date__range=[initial_date, end_date],
        ).order_by("dates")

        ordenadas = list(ordenadas)

        return ordenadas
