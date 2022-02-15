from distribuidor_dj.apps.auth.utils import user_in_commerce_group

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login


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


class AdminDashboardPassessTest(DashboardPassesTestMixin):
    permission_denied_message = (
        "Ingresa como administrador para ver el dashboard"
    )

    def test_func(self) -> bool:
        # Do not allow users that are not django administrators
        return self.request.user.is_staff
