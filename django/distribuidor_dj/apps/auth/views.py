"""
Extended Authentication views
"""
from distribuidor_dj.utils.const import CLIENT_GROUP_NAME, COMMERCE_GROUP_NAME

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.urls.base import reverse
from django.views.generic import CreateView
from django.views.generic.base import RedirectView

from .utils import user_in_commerce_group


class LoginView(auth_views.LoginView):
    """
    Extend/Override LoginView
    """

    template_name = "auth/login.html"
    next_page = "/accounts/login-proxy"


class LoginOutView(RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        logout(request)
        return response


class LoginProxyView(RedirectView):
    """
    View for redirecting succesfull logins
    """

    def get_redirect_url(self, *args, **kwargs):
        if user_in_commerce_group(self.request):
            return reverse("dashboard:index")
        elif self.request.user.groups.filter(name=CLIENT_GROUP_NAME).exists():
            return reverse("home")
        elif self.request.user.is_staff:
            return reverse("dashboard:adminshipments")
        return super().get_redirect_url(*args, **kwargs)


class RegisterUserView(CreateView):
    template_name = "auth/register.html"
    success_url = reverse_lazy("dashboard:index")
    form_class = UserCreationForm

    def form_valid(self, form: UserCreationForm):
        response = super().form_valid(form)
        user = self.object
        group = Group.objects.get(name=COMMERCE_GROUP_NAME)
        # Register use as commerce
        user.groups.add(group)
        # Login user
        login(self.request, user)

        return response

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # If the user is authenticated log out
        if self.request.user.is_authenticated:
            logout(self.request)
            messages.error(self.request, "Haz sido des-logueado")
        return response
