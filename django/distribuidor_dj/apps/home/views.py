from distribuidor_dj.apps.shipment.models import Shipment

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import TrackingForm


# Create your views here.
def home_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {}
        context["form"] = TrackingForm()
        if len(request.GET) > 0:
            form = TrackingForm(data=request.GET)
            if form.is_valid():
                try:
                    shipment = Shipment.objects.get(
                        id=form.cleaned_data["tracking_id"]
                    )
                    return render(
                        request,
                        "tracking/result.html",
                        {"shipment": shipment, "form": form},
                    )
                except Shipment.DoesNotExist:
                    return render(
                        request,
                        "tracking/index.html",
                        {
                            "form": form,
                            "notFound": True,
                            "notFoundMessage": "No se encontró el tracking",
                        },
                    )
            else:
                return render(request, "tracking/index.html", {"form": form})

        return render(request, "home.html", context)


def tracking_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {}
        context["form"] = TrackingForm()
        if len(request.GET) > 0:
            form = TrackingForm(data=request.GET)
            if form.is_valid():
                try:
                    shipment = Shipment.objects.get(
                        id=form.cleaned_data["tracking_id"]
                    )
                    return render(
                        request,
                        "tracking/result.html",
                        {"shipment": shipment, "form": form},
                    )
                except Shipment.DoesNotExist:
                    return render(
                        request,
                        "tracking/index.html",
                        {
                            "form": form,
                            "notFound": True,
                            "notFoundMessage": "No se encontró el tracking",
                        },
                    )
            else:
                return render(request, "tracking/index.html", {"form": form})

        return render(request, "tracking/index.html", context)


def tracking_result_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        context = {}
        context["form"] = TrackingForm()
        if len(request.GET) > 0:
            form = TrackingForm(data=request.GET)
            if form.is_valid():
                try:
                    shipment = Shipment.objects.get(
                        id=form.cleaned_data["tracking_id"]
                    )
                    return render(
                        request,
                        "tracking/result.html",
                        {"shipment": shipment, "form": form},
                    )
                except Shipment.DoesNotExist:
                    return render(
                        request,
                        "tracking/index.html",
                        {
                            "form": form,
                            "notFound": True,
                            "notFoundMessage": "No se encontró el tracking",
                        },
                    )
            else:
                return render(request, "tracking/result.html", {"form": form})

        return render(request, "tracking/result.html", context)
