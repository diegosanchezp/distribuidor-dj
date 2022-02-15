from django import template
from django.db.models import TextChoices

register = template.Library()


@register.simple_tag
def get_textchoice_label(value: str, textchoiceclass: TextChoices) -> str:
    return textchoiceclass[value].label
