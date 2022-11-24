# -*- coding: utf-8 -*-
"""TV_Series views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, create_access_token, current_user
from sqlalchemy.exc import IntegrityError

from nomad.database import db
from nomad.exceptions import InvalidUsage
from .models import TVSeries
from .serializers import tvserie_schema, tvseries_schema

blueprint = Blueprint('tv_series', __name__)


@blueprint.route('/api/tvseries', methods=('POST',))
@use_kwargs(tvserie_schema)
@marshal_with(tvserie_schema)
def add_movie(**kwargs):
    tconst = kwargs.pop('tconst', None)
    try:
        movie = TVSeries(tconst=tconst, **kwargs).save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.movie_already_exist()
    return movie


@blueprint.route('/api/movies/<int:tvseries_id>', methods=('GET',))
@use_kwargs(tvserie_schema)
@marshal_with(tvserie_schema)
def get_movie(movie_id: int):
    movie = TVSeries.query.filter_by(id=movie_id).first()
    return movie


@blueprint.route('/api/tvseries', methods=('GET',))
@use_kwargs(tvseries_schema)
@marshal_with(tvseries_schema)
def get_movies(**kwargs):
    movies = TVSeries.query.all()
    return movies
