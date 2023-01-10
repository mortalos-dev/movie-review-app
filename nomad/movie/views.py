# -*- coding: utf-8 -*-
"""Movies views."""

from flask import Blueprint, request
from flask_apispec import use_kwargs, marshal_with
from .serializers import movie_schema, movies_schema
from .controllers import GetMovieById, WriteMovie, GetAllMovies

blueprint = Blueprint('movies', __name__)


@blueprint.route('/api/movie', methods=('POST',))
@use_kwargs(movie_schema)
@marshal_with(movie_schema)
def add_movie(**kwargs):
    return WriteMovie().call(**kwargs)


@blueprint.route('/api/movies', methods=('POST',))
@use_kwargs(movie_schema)
@marshal_with(movie_schema)
def add_movies(**kwargs):
    return WriteMovie().call(**kwargs)


@blueprint.route('/api/movie', methods=('GET',))
@marshal_with(movie_schema)
def get_movie(**kwargs):
    return GetMovieById().call(**kwargs)


@blueprint.route('/api/movies', methods=('GET',))
@marshal_with(movies_schema)
def get_movies(**kwargs):
    return GetAllMovies().call(**kwargs)
