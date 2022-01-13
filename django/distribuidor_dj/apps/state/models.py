from enum import Enum
from typing import Callable

from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class StateMachineModel(models.Model):
    """
    Base class for models that neet state management
    Requieres a machine prop definition and a state char field
    """

    machine = {}

    def transition(
        self, event: Enum, fn: Callable[["StateMachineModel"], None]
    ) -> None:
        """
        Make a transition to the next state given the
        current state of the approval and a event
        """
        try:
            next_state = self.machine[self.state][event]
            if next_state:
                fn(self)
                self.state = next_state
        except KeyError:
            raise Exception(
                (
                    f"Error: no transition defined for state: {self.state}"
                    f"with event: {event.name}"
                )
            ) from KeyError

    class Meta:
        abstract = True


class StatusDate(models.Model):
    status = models.TextField(_("Estatus"))  # string
    date = models.DateField(_("Fecha"))

    class Meta:
        abstract = True
