import logging
from logging.config import dictConfig

from flask.logging import default_handler
from flask import Flask

from app.config import LOGGING

dictConfig(LOGGING)
app = Flask(__name__)

app.logger = logging.getLogger('movie-review-app')
app.logger.removeHandler(default_handler)
