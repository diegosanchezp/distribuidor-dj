from distribuidor_dj.apps.shipment import views as shviews

from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("shipments/", views.ShipmentsView.as_view(), name="shipments"),
    path("invoices/", views.InvoicesView.as_view(), name="invoices"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path(
        "admin-shipments",
        shviews.AdminDashShipmentList.as_view(),
        name="adminshipments",
    ),
]
