"""
Extended Authentication views
"""
from django.contrib.auth import views as auth_views


class LoginView(auth_views.LoginView):
    """
    Extend/Override LoginView
    """

    template_name = "auth/login.html"
