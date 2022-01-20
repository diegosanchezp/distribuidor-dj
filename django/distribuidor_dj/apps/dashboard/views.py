"""
Dashboard views
"""
from django.views.generic import TemplateView

from .mixins import DashboardPassesTestMixin


class Index(DashboardPassesTestMixin, TemplateView):
    template_name = "dashboard/index.html"
