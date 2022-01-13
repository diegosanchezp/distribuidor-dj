# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """
    Extends the django user model, with our custom attributes
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{str(self.user)}"
