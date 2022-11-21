# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask

from app.settings import ProdConfig
from app.extensions import bcrypt, cache, db, migrate, jwt, cors
from app import user, profile, movie, tv_series, comment


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(profile.views.blueprint, origins=origins)
    cors.init_app(movie.views.blueprint, origins=origins)
    cors.init_app(tv_series.views.blueprint, origins=origins)
    cors.init_app(comment.views.blueprint, origins=origins)

    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(movie.views.blueprint)
    app.register_blueprint(tv_series.views.blueprint)
    app.register_blueprint(comment.views.blueprint)

