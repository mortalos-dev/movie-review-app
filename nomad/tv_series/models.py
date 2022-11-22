# coding: utf-8

from nomad.database import (Model, SurrogatePK, db)


class TVSeries(Model, SurrogatePK):
    __tablename__ = 'tv_series'

    tconst = db.Column(db.String(12), unique=True, nullable=False)
    primaryTitle = db.Column(db.String(100))
    originalTitle = db.Column(db.String(100))
    description = db.Column(db.Text)
    isAdult = db.Column(db.Integer)
    startYear = db.Column(db.Integer)
    endYear = db.Column(db.Integer)
    linkToPic = db.Column(db.String(200))
    linkToTrailer = db.Column(db.String(100))
    genres = db.Column(db.String(50))
    runtimeMinutes = db.Column(db.Integer)
    actors = db.Column(db.String(100))
    directors = db.Column(db.String(100))
    averageRating = db.Column(db.Float)
    numVotes = db.Column(db.Integer)

    def __init__(self, tconst, **kwargs):
        db.Model.__init__(self, tconst=tconst, **kwargs)
