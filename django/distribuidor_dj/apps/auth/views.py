"""
Extended Authentication views
"""
from distribuidor_dj.utils.const import CLIENT_GROUP_NAME

from django.contrib.auth import views as auth_views
from django.urls.base import reverse
from django.views.generic.base import RedirectView

from .utils import user_in_commerce_group


class LoginView(auth_views.LoginView):
    """
    Extend/Override LoginView
    """

    template_name = "auth/login.html"
    next_page = "/accounts/login-proxy"


class LoginProxyView(RedirectView):
    """
    View for redirecting succesfull logins
    """

    def get_redirect_url(self, *args, **kwargs):
        if user_in_commerce_group(self.request):
            return reverse("dashboard:index")
        elif self.request.user.groups.filter(name=CLIENT_GROUP_NAME).exists():
            return reverse("home")
        return super().get_redirect_url(*args, **kwargs)
