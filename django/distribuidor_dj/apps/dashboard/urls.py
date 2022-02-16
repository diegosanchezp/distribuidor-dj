from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("shipments/", views.ShipmentsView.as_view(), name="shipments"),
    path("invoices/", views.InvoicesView.as_view(), name="invoices"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path("tracking/", views.TrackingView.as_view(), name="tracking"),
    path(
        "tracking-result/",
        views.TrackingResultView.as_view(),
        name="tracking-result",
    ),
    path(
        "invoice-detail/",
        views.InvoiceDetailView.as_view(),
        name="invoice-detail",
    ),
]
