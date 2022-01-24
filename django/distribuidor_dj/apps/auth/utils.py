"""
Authentication utils
"""
from distribuidor_dj.utils.const import COMMERCE_GROUP_NAME

from django.http.request import HttpRequest


def user_in_commerce_group(request: HttpRequest) -> bool:
    return request.user.groups.filter(name=COMMERCE_GROUP_NAME).exists()
