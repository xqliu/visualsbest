from flask import Flask

import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception

app = Flask(__name__)

@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        # access token for the demo app: https://rollbar.com/demo
        '90a56a42d47d4343a45b1105338d47c8',
        # environment name
        'heroku_development',
        # server root directory, makes tracebacks prettier
        root=os.path.dirname(os.path.realpath(__file__)),
        # flask already sets up logging
        allow_logging_basic_config=False)

    # send exceptions from `app` to rollbar, using flask's signal system.
    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


@app.route("/")
def hello():
    return "Hello World!, <a href='static/index.html'>click here</a> for UI demo"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
