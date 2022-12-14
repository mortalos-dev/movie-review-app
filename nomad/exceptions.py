from flask import jsonify


def template(data, code=500):
    return {'message': {'errors': {'body': data}}, 'status_code': code}


USER_NOT_FOUND = template(['User not found'], code=404)
USER_ALREADY_REGISTERED = template(['User already registered'], code=422)
UNKNOWN_ERROR = template([], code=500)
ARTICLE_NOT_FOUND = template(['Article not found'], code=404)
COMMENT_NOT_OWNED = template(['Not your article'], code=422)
MOVIE_ALREADY_EXIST = template(['Movie already exist'], code=422)
MOVIE_NOT_FOUND = template(['Movie not found'], code=404)
DATA_VALIDATION_ERROR = template(['Data not valid method type'], code=422)


class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_json(self):
        rv = self.message
        return jsonify(rv)

    @classmethod
    def user_not_found(cls):
        return cls(**USER_NOT_FOUND)

    @classmethod
    def user_already_registered(cls):
        return cls(**USER_ALREADY_REGISTERED)

    @classmethod
    def unknown_error(cls):
        return cls(**UNKNOWN_ERROR)

    @classmethod
    def article_not_found(cls):
        return cls(**ARTICLE_NOT_FOUND)

    @classmethod
    def comment_not_owned(cls):
        return cls(**COMMENT_NOT_OWNED)

    @classmethod
    def movie_already_exist(cls):
        return cls(**MOVIE_ALREADY_EXIST)

    @classmethod
    def data_validate_error(cls):
        return cls(**DATA_VALIDATION_ERROR)

    @classmethod
    def movie_not_found(cls):
        return cls(**MOVIE_NOT_FOUND)
