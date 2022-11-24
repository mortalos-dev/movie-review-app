# coding: utf-8
"""Movie models."""
from nomad.database import (Model, SurrogatePK, db, reference_col, relationship)


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
        """Create instance."""
        db.Model.__init__(self, tconst=tconst, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Movie({tconst!r})>'.format(tconst=self.tconst)


class Genre(Model, SurrogatePK):
    __tablename__ = 'genres'

    # id is needed for primary join, it does work with SurrogatePK class
    id = db.Column(db.Integer, primary_key=True)

    genre = db.Column(db.String(20), nullable=False)

    movie_id = reference_col('movies', nullable=False)
    movie = relationship('Movie', backref=db.backref('genres'))

    def __init__(self, genre, **kwargs):
        db.Model.__init__(self, genre=genre, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Genre({genre!r})>'.format(genre=self.genre)


class Actor(Model, SurrogatePK):
    __tablename__ = 'actors'

    # id is needed for primary join, it does work with SurrogatePK class
    id = db.Column(db.Integer, primary_key=True)

    actor = db.Column(db.String(20), nullable=False)

    movie_id = reference_col('movies', nullable=False)
    movie = relationship('Movie', backref=db.backref('actor'))

    def __init__(self, actor, **kwargs):
        db.Model.__init__(self, actor=actor, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Actor({actor!r})>'.format(actor=self.actor)
