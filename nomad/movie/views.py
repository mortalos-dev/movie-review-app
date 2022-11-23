# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, create_access_token, current_user
from sqlalchemy.exc import IntegrityError

from nomad.database import db
from nomad.exceptions import InvalidUsage
from .models import Movie
from .serializers import movie_schema, movies_schema

blueprint = Blueprint('movies', __name__)


@blueprint.route('/api/movies', methods=('POST',))
@use_kwargs(movie_schema)
@marshal_with(movie_schema)
def add_movie(**kwargs):
    tconst = kwargs.pop('tconst', None)
    print(kwargs, tconst)
    try:
        movie_item = Movie(tconst=tconst, **kwargs).save()
    except IntegrityError:
        db.session.rollback()
        raise InvalidUsage.movie_already_exist()
    return movie_item


@blueprint.route('/api/movies/<int:movie_id>', methods=('GET',))
@use_kwargs(movie_schema)
@marshal_with(movie_schema)
def get_movie(movie_id: int):
    movie = Movie.query.filter_by(id=movie_id).first()
    return movie


@blueprint.route('/api/movies', methods=('GET',))
@use_kwargs(movies_schema)
@marshal_with(movies_schema)
def get_movies(**kwargs):
    movies = Movie.query.all()
    return movies
