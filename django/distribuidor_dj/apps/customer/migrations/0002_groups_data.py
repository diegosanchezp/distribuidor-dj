# Generated by Django 4.0 on 2022-01-14 19:39

from distribuidor_dj.utils import const

from django.apps.registry import Apps
from django.db import migrations


def create_initial_groups(apps: Apps, schema_editor):
    """
    Create inital needed group for the app
    """
    Group = apps.get_model("auth", "Group")
    Group.objects.create(name=const.COMMERCE_GROUP_NAME)
    Group.objects.create(name=const.CLIENT_GROUP_NAME)


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0001_initial"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [migrations.RunPython(create_initial_groups)]
