# coding: utf-8

from marshmallow import (Schema, fields, pre_load, post_dump, validate, ValidationError)
from nomad.exceptions import InvalidUsage
from nomad.utils import custom_data_filter


class MovieSchema(Schema):
    tconst = fields.Str(required=True, validate=validate.Length(min=9, max=11))
    primary_title = fields.Str(required=True)
    original_title = fields.Str(required=True)
    description = fields.Str()
    adult = fields.Boolean()
    year = fields.Int(required=True)
    genres = fields.Str()
    pic = fields.Url()
    trailer = fields.Url()
    duration = fields.Int()
    actors = fields.Str()
    directors = fields.Str()
    rating = fields.Float(required=True)
    votes = fields.Int(required=True)
    # ugly hack.
    # movie = fields.Nested('self', exclude=('movie',), default=True, load_only=True)

    @pre_load
    def load_movie(self, data, **kwargs):
        data = data.get('movie')
        if data is None:
            raise InvalidUsage.data_validate_error()
        # some of the frontends send this like an empty string and some send
        # null
        if not data.get('tconst', True):
            del data['tconst']
        if not data.get('is_adult', True):
            del data['adult']

        if data.get('actors'):
            items = data.get('actors').split(',')
            data['actors'] = ','.join(list(filter(lambda x: x, items)))
        if data.get('directors'):
            items = data.get('directors').split(',')
            data['directors'] = ','.join(list(filter(lambda x: x, items)))
        year = data.get('year')
        if not year:
            del data['year']
        return data

    @post_dump
    def dump_movie(self, data, **kwargs):
        print('Post Dump one movie')
        # data = custom_data_filter(data)
        return {'movie': data}

    @post_dump(pass_many=True)
    def dump_movies(self, data, **kwargs):
        print('Post Dump many movies')
        return data

    class Meta:
        strict = True


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
