import uuid
from enum import Enum
from typing import Callable, Optional, Type

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

StateAction = Optional[Callable[["StateMachineModel"], None]]


class StateMachineModel(models.Model):
    """
    Base class for models that neet state management
    Requieres a machine prop definition and a state char field
    """

    # Todo validate that these fields are not none
    machine: dict[Enum, dict[Enum, Enum]]
    status_date_class: Type["StatusDate"]
    status_date_relattr: str

    class Meta:
        abstract = True

    def transition(self, event: Enum, fn: StateAction = None) -> None:
        """
        Make a transition to the next state given the
        current state of the approval and a event
        """
        try:
            next_state = self.machine[self.state][event]
            if next_state:
                if fn:
                    fn(self)
                self.state = next_state
        except KeyError:
            raise Exception(
                (
                    f"Error: no transition defined for state: {self.state}"
                    f"with event: {event.name}"
                )
            ) from KeyError

    def transition_set_date(
        self, event: Enum, fn: StateAction = None
    ) -> "StatusDate":
        """
        Helper method to transition state and set date of the state transition
        """
        self.transition(event, fn)
        # status_date_class is a class that inherits from StatusDate
        # We create a instance an set its attribute that relates to
        # this "self" model
        sd = self.status_date_class(status=self.state)
        setattr(sd, self.status_date_relattr, self)
        return sd


class StatusDate(models.Model):
    status = models.TextField(_("Estatus"))  # string
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(
        _("Fecha"),
        auto_now_add=True,
    )

    class Meta:
        abstract = True
