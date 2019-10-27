import os
import flask
import google_auth


os.environ.setdefault("FN_AUTH_REDIRECT_URI","http://localhost:8040/google/auth")
os.environ.setdefault("FN_BASE_URI","http://localhost:8040")
os.environ.setdefault("FN_CLIENT_ID","183079298451-mhjb15qu6mpmvecprsvl8knlk7ov20hc.apps.googleusercontent.com")
os.environ.setdefault("FN_CLIENT_SECRET","CE_9ec7KN9kwqnV0JXx0Lx9h")

os.environ.setdefault("FLASK_APP","app.py")
os.environ.setdefault("FLASK_DEBUG",1)
os.environ.setdefault("FN_FLASK_SECRET_KEY","1234567")

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.app)


@app.route('/')
def index():
    if google_auth.is_logged_in():

        return flask.render_template('list.html', user_info=google_auth.get_user_info())

    return 'You are not currently logged in.'