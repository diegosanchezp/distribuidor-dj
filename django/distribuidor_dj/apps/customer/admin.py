from django.contrib import admin  # noqa F401

from .models import Customer

# Register your models here.
admin.site.register(Customer)
