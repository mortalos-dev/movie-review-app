# coding: utf-8

from marshmallow import (Schema, fields, pre_load, post_dump, validate, ValidationError)
from nomad.exceptions import InvalidUsage


class TVSeriesSchema(Schema):
    tconst = fields.Str(required=True, validate=validate.Length(min=9, max=11))
    primary_title = fields.Str(required=True)
    original_title = fields.Str(required=True)
    description = fields.Str()
    is_adult = fields.Boolean()
    start_year = fields.Int(required=True)
    pic_link = fields.Url()
    trailer_link = fields.Url()
    genres = fields.Str(required=True)
    runtime_minutes = fields.Int()
    actors = fields.Str()
    directors = fields.Str()
    average_rating = fields.Float(required=True)
    num_votes = fields.Int(required=True)

    @pre_load
    def load_tvseries(self, data, **kwargs):
        data = data.get('tv_series')
        if data is None:
            raise InvalidUsage.data_validate_error()
        # some of the frontends send this like an empty string and some send
        # null
        if not data.get('tconst', True):
            del data['tconst']
        if not data.get('is_adult', True):
            data['is_adult'] = 0
        return data

    @post_dump
    def dump_tvseries(self, data, **kwargs):
        data = custom_data_filter(data)
        return {'tv_series': data}

    class Meta:
        strict = True


tvserie_schema = TVSeriesSchema()
tvseries_schema = TVSeriesSchema(many=True)
