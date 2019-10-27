import os
import flask
import google_auth
import cal, gmail, twitter, calUtils
from flask import render_template, redirect

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.app)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    cal.main()
    s, e = cal.create_calendar_matrix()

    twitterInfo = twitter.getCalendar('jalfrazi_')
    gmailInfo = gmail.getLastSent()
    labels = calUtils.getMonthLabels()

    return render_template('dashboard.html', slots=s, events=e, twitterInfo=twitterInfo[::-1], gmailInfo=gmailInfo[::-1])


@app.route('/')
def index():
    if google_auth.is_logged_in():
        return render_template('dashboard.html', user_info=google_auth.get_user_info())
    else:
        return redirect('/google/login')

    return 'You are not currently logged in.'
