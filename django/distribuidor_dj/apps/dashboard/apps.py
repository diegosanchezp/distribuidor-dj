import os

from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "distribuidor_dj.apps.dashboard"

    def ready(self):
        from django_q.cluster import Cluster

        if os.environ.get("RUN_MAIN", None) != "true":
            q = Cluster()
            q.start()
