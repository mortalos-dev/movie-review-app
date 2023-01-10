# coding: utf-8
"""Movie controllers."""
from flask import make_response, request
from .models import Movie, Genre, Actor, Director
from nomad.exceptions import InvalidUsage
from sqlalchemy.exc import IntegrityError
from nomad.database import db
from flask import current_app


class BaseController:
    def __init__(self):
        self.request = request

    def call(self, *args, **kwargs):
        try:
            current_app.logger.info(f"Started {self.__class__.__name__}")
            return self._call(*args, **kwargs)
        except InvalidUsage as ex:
            current_app.logger.exception(f"Error in call method of controller: {ex}")
            raise
        except Exception as ex:
            current_app.logger.exception(f"Error in call method of controller: {ex}")
            return make_response(str(ex), getattr(ex, "code", 500))

    def _call(self, *args, **kwargs):
        raise NotImplementedError("_call")


class GetMovieById(BaseController):

    def _call(self, *args, **kwargs):
        # res = requests.get('http://127.0.0.1:5000/api/movie/?tconst=tt0000001')  ###EXAMPLE###
        tconst = self.request.args.get('tconst')
        movie_id = self.request.args.get('movie_id')
        current_app.logger.info(f"Get parameters from request {tconst, movie_id} ")
        if tconst:
            movie = Movie.query.filter_by(tconst=str(tconst)).first()
            if movie:
                return movie
        if movie_id:
            movie = Movie.query.filter_by(id=int(movie_id)).first()
            if movie:
                return movie

        raise InvalidUsage.movie_not_found()


class WriteMovie(BaseController):

    def _call(self, *args, **kwargs):
        tconst = kwargs.pop('tconst', None)
        actors = kwargs.pop('actors', None)
        genres = kwargs.pop('genres', None)
        directors = kwargs.pop('directors', None)
        current_app.logger.debug(f"parameters after pop items {tconst, genres, actors, directors} ")

        try:
            self.movie = Movie.query.filter_by(tconst=tconst).first()
            if not self.movie:
                self.movie = Movie(tconst=tconst, **kwargs).save(commit=False)

            current_app.logger.debug(f"call genres {genres} ")

            genre_items = self._db_table_update('genre', 'nomad.movie.models.Genre', genres)
            if genre_items:
                self.movie.genres.extend(genre_items)

            actor_items = self._db_table_update('actor', 'nomad.movie.models.Actor', actors)
            if actor_items:
                self.movie.actors.extend(actor_items)

            director_items = self._db_table_update('director', 'nomad.movie.models.Director', directors)
            if director_items:
                self.movie.directors.extend(director_items)

            self.movie.save()

            current_app.logger.info(f'Ended {self.__class__.__name__}')

        except IntegrityError as ex:
            current_app.logger.exception("Error: %s" % ex)
            db.session.rollback()
            raise InvalidUsage.movie_already_exist()

        return self.movie.query.filter_by(tconst=tconst).first()

    def _db_table_update(self, col_name: str, model_name: str, items_str=None):
        if not items_str:
            current_app.logger.debug(f"There are no elements in model list {model_name}")
            return

        # check updates in table
        items_in = set(items_str.split(','))
        model_cls = self._factory(model_name)
        items_db = model_cls.query.filter_by(movie_id=self.movie.id).all()

        if items_db:
            items_db_set = {item.__dict__[col_name] for item in items_db}
        else:
            items_db_set = set()

        need_delete = items_db_set - items_in
        need_add = items_in - items_db_set
        current_app.logger.debug(f'new items = {items_in}, db items = {items_db_set}, '
                                 f'intersection = {items_db_set & items_in} '
                                 f'need new items = {need_add} '
                                 f'delete items = {need_delete}')

        if need_delete:
            model_cls.query.\
                filter_by(movie_id=self.movie.id).\
                filter(getattr(model_cls, col_name).in_(need_delete)).\
                delete()

        item_list = []
        for item in need_add:
            item_field = dict()
            key = (str(model_cls.__dict__[col_name])).split('.')[1]
            item_field[key] = item
            item_field['movie_id'] = self.movie.id
            current_app.logger.debug(f"Item fields  {item_field}")
            item_add = model_cls(**item_field).save()
            current_app.logger.debug(f"Items added  {item_add}")
            item_list.append(item_add)
        return item_list

    @staticmethod
    def _factory(class_str):
        try:
            from importlib import import_module
            *module_path, class_name = class_str.rsplit('.', 1)
            current_app.logger.debug(f"Path to model - {module_path}, class name - {class_name}")
            module = import_module('.'.join(module_path))
            return getattr(module, class_name)
        except (ImportError, AttributeError) as ex:
            current_app.logger.exception("Error: %s" % ex)
            raise ImportError(class_str)


class GetAllMovies(BaseController):

    def _call(self, *args, **kwargs):
        movies = Movie.query.filter_by(**kwargs).all()
        current_app.logger.debug(f"movies.genres {movies[0].genres, type(movies[0].genres)}")
        return movies
