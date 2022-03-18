from distribuidor_dj.apps.auth.utils import user_in_commerce_group

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect
from django.urls import reverse_lazy


class DashboardPassesTestMixin(UserPassesTestMixin):
    """
    Reusable UserPassesTestMixin for the dashboard views
    to be used in class based views
    """

    permission_denied_message = (
        "Ingresa como usuario juridico para ver el dashboard"
    )
    login_url = "/accounts/login"

    def test_func(self) -> bool:
        # Do not allow users that are not in the commerce group name
        return user_in_commerce_group(self.request)

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect_to_login(
            self.request.get_full_path(),
            self.get_login_url(),
            self.get_redirect_field_name(),
        )


class ShipmentDetailTest(UserPassesTestMixin):
    """
    Checks that the Shipment belogs to the
    commerce that is trying to read it
    """

    permission_denied_message = (
        "El envio no fue crado por ti, por lo tanto no puedes verlo"
    )

    login_url = reverse_lazy("dashboard:shipments")

    def test_func(self) -> bool:
        # Do not allow users that are not in the commerce group name
        shipment = self.get_object()
        return shipment.commerce == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(self.login_url)


class InvoiceDetailTest(ShipmentDetailTest):
    """
    Checks that the Shipment belogs to the
    commerce that is trying to read it
    """

    permission_denied_message = "La factura no te pertenece"

    login_url = reverse_lazy("dashboard:invoices")


class AdminDashboardPassessTest(DashboardPassesTestMixin):
    permission_denied_message = (
        "Ingresa como administrador para ver el dashboard"
    )

    def test_func(self) -> bool:
        # Do not allow users that are not django administrators
        return self.request.user.is_staff
