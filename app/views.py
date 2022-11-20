from app import app
import controllers


@app.route("/")
def hello():
    return "Hello everybody!"


@app.route("/logs/<log_type>")
def view_logs(log_type):
    return controllers.ViewLogs().call(log_type)