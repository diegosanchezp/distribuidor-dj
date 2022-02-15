# Create your views here.
from distribuidor_dj.apps.dashboard.mixins import AdminDashboardPassessTest
from distribuidor_dj.apps.dashboard.views import ShipmentsView

from django import forms
from django.db.models.query import QuerySet
from django.urls.base import reverse_lazy
from django.views.generic.edit import UpdateView

from .models import Shipment


class AdminDashShipmentList(AdminDashboardPassessTest, ShipmentsView):
    template_name = "shipments/admin_shipments.html"
    paginate_by = 2  # change this later to 10
    extra_context = {"shipment_detail_url": "dashboard:admin-shipment-detail"}

    def get_queryset(self) -> "QuerySet[Shipment]":
        queryset = Shipment.objects.all()
        queryset = self.apply_search(queryset)
        return queryset


class TransitionShipmentForm(forms.ModelForm):
    action = forms.TypedChoiceField(
        choices=Shipment.Events.choices, coerce=str
    )

    class Meta:
        model = Shipment
        fields = ["state"]


class AdminShipmentDetail(AdminDashboardPassessTest, UpdateView):
    """
    - Displays shipment data
    - Makes shipment state transition
    """

    model = Shipment
    template_name = "shipments/admin_shipment_detail.html"
    success_url = reverse_lazy("dashboard:index")
    context_object_name = "shipment"
    slug_field = "id"
    extra_context = {
        "statechoices": Shipment.States,
        "stateactions": Shipment.Events,
    }
    model = Shipment
    form_class = TransitionShipmentForm

    def get_template_names(self):
        if self.request.htmx and self.request.method == "POST":
            return ["shipments/admin/state_transition.html"]
        else:
            return super().get_template_names()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        stateaction_map = {
            str(Shipment.States.CREATED): {
                "stateaction": Shipment.Events.ON_SEND,
                "text": "Enviar",
            },
            str(Shipment.States.SENDED): {
                "stateaction": Shipment.Events.ON_RECIEVE,
                "text": "Marcar como recibido",
            },
        }
        ctx["action_map"] = stateaction_map.get(self.get_object().state)
        return ctx

    def form_valid(self, form):
        # Return html partial instead of whole page
        shipment: "Shipment" = self.object
        status_date = shipment.transition_set_date(
            Shipment.Events[form.cleaned_data["action"]]
        )
        status_date.save()
        shipment.save()

        return self.render_to_response(
            self.get_context_data(form=self.form_class(instance=shipment))
        )
