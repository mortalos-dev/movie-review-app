from nomad import app
from flask import request, make_response, render_template
from models import ErrorLog


class BaseController:
    def __init__(self):
        self.request = request

    def call(self, *args, **kwds):
        try:
            app.logger.info(f"Started {self.__class__.__name__}")
            return self._call(*args, **kwds)
        except Exception as ex:
            app.logger.exception("Error: %s" % ex)
            return make_response(str(ex), getattr(ex, "code", 500))

    def _call(self, *args, **kwds):
        raise NotImplementedError("_call")


class ViewLogs(BaseController):
    def _call(self, log_type):
        app.logger.debug("log_type: %s" % log_type)
        page = int(self.request.args.get("page", 1))
        logs_map = {"error": ErrorLog}

        if log_type not in logs_map:
            raise ValueError("Unknown log_type: %s" % log_type)

        log_model = logs_map[log_type]
        logs = log_model.select().paginate(page, 10).order_by(log_model.id.desc())
        return render_template("logs.html", logs=logs)