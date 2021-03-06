"""distribuidor_dj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from distribuidor_dj.apps.home.views import home_view

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .apps.home import views

urlpatterns = [
    path("", home_view, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include("distribuidor_dj.apps.api.urls")),
    path("accounts/", include("distribuidor_dj.apps.auth.urls")),
    path(
        "dashboard/",
        include("distribuidor_dj.apps.dashboard.urls", namespace="dashboard"),
    ),
    path("tracking/", views.tracking_view, name="tracking"),
    path(
        "tracking-result",
        views.tracking_result_view,
        name="tracking-result",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
