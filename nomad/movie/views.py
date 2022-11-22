# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, create_access_token, current_user
from sqlalchemy.exc import IntegrityError

from nomad.database import db
from nomad.exceptions import InvalidUsage
from .models import Movie
from .serializers import movie_schema, movie_schemas

blueprint = Blueprint('movies', __name__)


@blueprint.route('/api/movie', methods=('POST',))
@use_kwargs(movie_schema)
@marshal_with(movie_schema)
def register_user(username, password, email, **kwargs):
    try:
        userprofile = Movie(username, email, password=password, **kwargs).save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.user_already_registered()
    return userprofile.user


@blueprint.route('/api/users/login', methods=('POST',))
@jwt_required(optional=True)
@use_kwargs(movie_schema)
@marshal_with(movie_schema)
def login_user(email, password, **kwargs):
    user = Movie.query.filter_by(email=email).first()
    if user is not None and user.check_password(password):
        user.token = create_access_token(identity=user, fresh=True)
        return user
    else:
        raise InvalidUsage.user_not_found()


@blueprint.route('/api/movie/<int:id>', methods=('GET',))
@marshal_with(movie_schema)
def get_movie(id: int):
    movie = Movie.query.first()

    return movie


@blueprint.route('/api/movie', methods=('GET',))
@use_kwargs(movie_schemas)
@marshal_with(movie_schemas)
def get_movies(**kwargs):
    user = current_user
    # take in consideration the password
    password = kwargs.pop('password', None)
    if password:
        user.set_password(password)
    if 'updated_at' in kwargs:
        kwargs['updated_at'] = user.created_at.replace(tzinfo=None)
    user.update(**kwargs)
    return user
