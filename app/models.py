# -*- coding: utf-8 -*-
"""App models."""
import datetime as dt

from app.database import (Model, SurrogatePK, db, Column)


class _Model(Model):

    def json(self):
        return self.__data__


class ErrorLog(_Model, SurrogatePK):
    __tablename__ = "error_logs"

    request_data = Column(db.Text, nullable=True)
    request_url = Column(db.Text, nullable=True)
    request_method = Column(db.String(100), nullable=True)
    error = Column(db.Text, nullable=True)
    traceback = Column(db.Text, nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)


class ApiLog(_Model):
    __tablename__ = "api_logs"

    request_url = Column(db.String(100), nullable=True)
    request_data = Column(db.Text, nullable=True)
    request_method = Column(db.String(100), nullable=True)
    request_headers = Column(db.Text, nullable=True)
    response_text = Column(db.Text, nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    finished_at = Column(db.DateTime, nullable=True, default=dt.datetime.utcnow)
    error = Column(db.Text, nullable=True)

