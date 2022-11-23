# coding: utf-8

from nomad.database import (Model, SurrogatePK, db)


class Movie(Model, SurrogatePK):
    __tablename__ = 'movies'

    tconst = db.Column(db.String(12), unique=True, nullable=False)
    primary_title = db.Column(db.String(100))
    original_title = db.Column(db.String(100))
    description = db.Column(db.Text)
    is_adult = db.Column(db.Integer)
    start_year = db.Column(db.Integer)
    pic_link = db.Column(db.String(200))
    trailer_link = db.Column(db.String(100))
    genres = db.Column(db.String(50))
    runtime_minutes = db.Column(db.Integer)
    actors = db.Column(db.String(100))
    directors = db.Column(db.String(100))
    average_rating = db.Column(db.Float)
    num_votes = db.Column(db.Integer)

    def __init__(self, tconst, **kwargs):
        db.Model.__init__(self, tconst=tconst, **kwargs)



