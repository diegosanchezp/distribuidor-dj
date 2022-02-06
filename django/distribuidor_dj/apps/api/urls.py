from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from django.urls import path

from .views import AddressStateViewSet, ShipmentViewSet

router = routers.SimpleRouter()

router.register(r"shipments", ShipmentViewSet)
router.register(r"address_state", AddressStateViewSet)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "docs/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]

urlpatterns += router.urls
