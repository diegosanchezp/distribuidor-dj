"""
Background tasks
"""

import datetime

# Write here functions you want to schedule.
from distribuidor_dj.apps.invoice.models import Invoice, InvoiceStatusDate

from django.db.models import DurationField, ExpressionWrapper, F, Q
from django.utils import timezone


def check_invoices():
    """
    Check for due invoices, does the check once an hour
    Runs if the django_q cluster is activated.
    """
    # Get invoices that are not overdue
    # Check invoices that might be overdue:
    # time elapsed from creation date to todays date
    # (date difference) is greater than 15 day
    # Reference https://stackoverflow.com/a/50601209
    overdue_invoices_dates = (
        InvoiceStatusDate.objects.filter(Q(status=Invoice.States.UNPAID))
        .annotate(
            # date_diff type is timedelta
            date_diff=ExpressionWrapper(
                timezone.now() - F("date"), output_field=DurationField()
            )
        )
        .filter(date_diff__gte=datetime.timedelta(days=15))
    )

    # invoice_dates = []

    # Set the OVERDUE status dates.
    for overdue_dt in overdue_invoices_dates:
        inv_sd = overdue_dt.invoice.transition_set_date(
            Invoice.Events.ON_OVERDUE
        )
        overdue_dt.invoice.save()
        inv_sd.save()

    #     overdue_invoices.update(state=Invoice.States.OVERDUE)
    #
    #     InvoiceStatusDate.objects.bulk_create(invoice_dates)
