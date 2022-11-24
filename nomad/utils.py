# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from nomad.user.models import User  # noqa


def jwt_identity(payload):
    return User.get_by_id(payload)


def identity_loader(user):
    return user.id


def custom_data_filter(data: dict):
    # filter for null and empty strings
    return dict(filter(lambda item: (item[1] is not None), data.items()))
