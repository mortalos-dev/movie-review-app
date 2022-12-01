# coding: utf-8
"""Movie models."""
from nomad.database import (Model, Column, SurrogatePK, db, reference_col, relationship)
import datetime as dt


class Movie(Model, SurrogatePK):
    __tablename__ = 'movies'

    tconst = Column(db.String(12), unique=True, nullable=False)
    primary_title = Column(db.String(100))
    original_title = Column(db.String(100))
    description = Column(db.Text)
    adult = Column(db.Integer)
    year = Column(db.Integer)
    pic = Column(db.String(200))
    trailer = Column(db.String(100))
    duration = Column(db.Integer)
    rating = Column(db.Float)
    votes = Column(db.Integer)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    updated_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    genres = relationship('Genre', backref='movies', lazy='dynamic')
    actors = relationship('Actor', backref='movies', lazy='dynamic')
    directors = relationship('Director', backref='movies', lazy='dynamic')

    def __init__(self, tconst, **kwargs):
        """Create instance."""
        db.Model.__init__(self, tconst=tconst, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Movie({tconst!r})>'.format(tconst=self.tconst)


class Genre(Model, SurrogatePK):
    __tablename__ = 'genres'

    genre = db.Column(db.String(20), nullable=False)
    movie_id = reference_col('movies', nullable=False)

    def __init__(self, genre, **kwargs):
        db.Model.__init__(self, genre=genre, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Genre({genre!r})>'.format(genre=self.genre)


class Actor(Model, SurrogatePK):
    __tablename__ = 'actors'

    actor = db.Column(db.String(20), nullable=False)
    movie_id = reference_col('movies', nullable=False)

    def __init__(self, actor, **kwargs):
        db.Model.__init__(self, actor=actor, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Actor({actor!r})>'.format(actor=self.actor)


class Director(Model, SurrogatePK):
    __tablename__ = 'directors'

    director = db.Column(db.String(20), nullable=False)
    movie_id = reference_col('movies', nullable=False)

    def __init__(self, director, **kwargs):
        db.Model.__init__(self, director=director, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Director({director!r})>'.format(director=self.director)
