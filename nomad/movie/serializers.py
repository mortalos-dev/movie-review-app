# coding: utf-8

from marshmallow import (Schema, fields, pre_load, post_load, pre_dump, post_dump, validate, ValidationError)
from .models import Movie
from nomad.exceptions import InvalidUsage
from flask import current_app


class BaseSchema(Schema):
    __envelope__ = {'single': None, 'many': None}
    __field_list__ = []  # list of fields
    __model__ = Movie

    def get_envelope_key(self, many: bool):
        """Helper to get the envelope key."""
        key = self.__envelope__['many'] if many else self.__envelope__['single']
        current_app.logger.debug(f"Envelope key == {key}")
        assert key is not None, "Envelope key undefined"
        return key

    def clear_data(self, data: dict) -> dict:
        if not self.__field_list__:
            current_app.logger.debug(f"Field list undefined == {self.__field_list__}")
        assert self.__field_list__ is not None, "Field list undefined"
        current_app.logger.debug(f"Data before clearing == {data}")
        new_data = map(self.del_empty_field, data, self.__field_list__)
        data = {key: value for key, value in new_data}
        current_app.logger.debug(f"Cleared data == {data}")
        return data

    def del_empty_field(self, data, key):
        if not data.get(key, True):
            del data[key]
        return data

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)

        current_app.logger.debug(f"Pre Load common {many, key}")
        if many:
            current_app.logger.debug(f"Pre Load many movies {data}")
        else:
            data = self.clear_data(data)
            current_app.logger.debug(f"Pre Load one movie {data}")
        return data[key]

    @pre_dump
    def clear_collection(self, data, **kwargs):
        current_app.logger.debug(f"Pre Dump one movie {type(data)}")
        return data

    @post_dump(pass_many=True)
    def wrap_with_envelope(self, data, many, **kwargs):
        key = self.get_envelope_key(many)
        current_app.logger.debug(f"Post Dump common {many, key}")
        if many:
            current_app.logger.debug(f"Post Dump many movies {len(data)}")
        else:
            current_app.logger.debug(f"Post Dump one movie {data['tconst']}")
        return {key: data}


class MovieSchema(BaseSchema):
    __envelope__ = {'single': 'movie', 'many': 'movies'}
    __field_list__ = ['tconst', 'primary_title', 'original_title', 'description', 'adult', 'year',
                      'genres', 'pic', 'trailer', 'duration', 'actors', 'directors', 'rating', 'votes']

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
    rating = fields.Float(validate=validate.Range(min=0, max=10))
    votes = fields.Int(validate=validate.Range(min=0))
    # ugly hack.
    # movie = fields.Nested('self', exclude=('movie',), default=True, load_only=True)

    class Meta:
        strict = True


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
