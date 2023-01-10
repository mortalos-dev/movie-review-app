# -*- coding: utf-8 -*-
"""The nomad module, containing the nomad factory function."""
from flask import Flask

from nomad.settings import ProdConfig
from nomad.extensions import bcrypt, cache, db, migrate, jwt, cors

from nomad.exceptions import InvalidUsage


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__.split('.')[0])     # nomad.app
    app.logger.info(f'flask name is {__name__}')
    app.logger.info(f'secret key get from venv - {config_object.SECRET_KEY}')
    app.url_map.strict_slashes = False
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    return app


def register_extensions(app):
    """Register Flask extensions."""
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_blueprints(app):
    from nomad import user, profile, movie, tv_series, review
    """Register Flask blueprints."""
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(user.views.blueprint, origins=origins)
    cors.init_app(profile.views.blueprint, origins=origins)
    cors.init_app(movie.views.blueprint, origins=origins)
    cors.init_app(tv_series.views.blueprint, origins=origins)
    # cors.init_app(review.views.blueprint, origins=origins)

    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(profile.views.blueprint)
    app.register_blueprint(movie.views.blueprint)
    app.register_blueprint(tv_series.views.blueprint)
    # app.register_blueprint(review.views.blueprint)


def register_errorhandlers(app):

    def errorhandler(error):
        response = error.to_json()
        response.status_code = error.status_code
        return response

    app.errorhandler(InvalidUsage)(errorhandler)


