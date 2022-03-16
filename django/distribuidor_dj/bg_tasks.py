"""
Background tasks
"""

import datetime

# Write here functions you want to schedule.
from distribuidor_dj.apps.invoice.models import Invoice

from django.db.models import DurationField, ExpressionWrapper, F, Q
from django.utils import timezone


def check_invoices():
    """
    Check for due invoices, does the check once an hour
    """
    # Get invoices that are not overdue
    # Check invoices that might be overdue:
    # time elapsed from creation date to todays date
    # (date difference) is greater than 15 day
    # Reference https://stackoverflow.com/a/50601209
    overdue_invoices = (
        Invoice.objects.filter(~Q(dates__status=Invoice.States.OVERDUE))
        .annotate(
            # date_diff type is timedelta
            date_diff=ExpressionWrapper(
                timezone.now() - F("dates__date"), output_field=DurationField()
            )
        )
        .filter(date_diff__gte=datetime.timedelta(days=15))
    )

    # invoice_dates = []

    # Set the OVERDUE status dates.
    for invoice in overdue_invoices:
        inv_sd = invoice.transition_set_date(Invoice.Events.ON_OVERDUE)
        invoice.save()
        inv_sd.save()

    #     overdue_invoices.update(state=Invoice.States.OVERDUE)
    #
    #     InvoiceStatusDate.objects.bulk_create(invoice_dates)

    """
    invoice -> 15/1/2022
    todays_date 30/1/2022
    todays_date - invoice >= 15 ? Yes
    """
