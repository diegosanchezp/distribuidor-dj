from distribuidor_dj.apps.shipment import views as shviews

from django.urls import path

from . import views

app_name = "dashboard"
urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("payments/", views.Payments.as_view(), name="payments"),
    path("shipments/", views.ShipmentsView.as_view(), name="shipments"),
    path("invoices/", views.InvoicesView.as_view(), name="invoices"),
    path("settings/", views.SettingsView.as_view(), name="settings"),
    path(
        "invoice-detail/<slug:pk>",
        views.InvoiceDetailView.as_view(),
        name="invoice-detail",
    ),
    path(
        "invoice-detail/",
        views.InvoiceDetailView.as_view(),
        name="invoice-detail-query",
    ),
    path("admin/", shviews.AdminDashIndex.as_view(), name="admin-index"),
    path(
        "admin/shipments/",
        shviews.AdminDashShipmentList.as_view(),
        name="adminshipments",
    ),
    path(
        "admin/reportes",
        views.ReportesView.as_view(),
        name="reportes",
    ),
    path(
        "shipment/<slug:pk>/",
        views.ShipmentDetail.as_view(),
        name="shipment-detail",
    ),
    path(
        "admin/shipment/<slug:pk>/",
        shviews.AdminShipmentDetail.as_view(),
        name="admin-shipment-detail",
    ),
    path(
        "admin/invoice-detail/<slug:pk>",
        views.AdminInvoiceDetailView.as_view(),
        name="admin-invoice-detail",
    ),
    path(
        "admin/invoices/",
        views.AdminInvoicesView.as_view(),
        name="admin-invoices",
    ),
]
