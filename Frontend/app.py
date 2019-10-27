import os
import flask
import google_auth

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():

        return flask.render_template('list.html', user_info=google_auth.get_user_info())

    return 'You are not currently logged in.'
