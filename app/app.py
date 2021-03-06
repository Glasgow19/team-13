import os
import flask
import google_auth
import sys
from flask import render_template, redirect

app = flask.Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)

app.register_blueprint(google_auth.app)

sys.path.insert(1, '../database/')
import cal, gmail, twitter, calUtils, recommendation

@app.route('/dashboard', methods=['GET'])
def dashboard():
    access = flask.session['auth_token']['access_token']
    cal.main(access)
    s, e = cal.create_calendar_matrix()

    twitterInfo = twitter.getCalendar('jalfrazi_')
    userInfo = google_auth.get_user_info()
    userId = userInfo['id']
    
    gmailInfo = gmail.getLastSent(access,userId)

    recommendations = recommendation.recommend()

    return render_template('dashboard.html', slots=s, events=e, twitterInfo=twitterInfo[::-1], gmailInfo=gmailInfo[::-1], user_info=userInfo, recommendations=recommendations)


@app.route('/')
def index():
    if google_auth.is_logged_in():
        return redirect('/dashboard')
    else:
        return redirect('/google/login')

    return 'You are not currently logged in.'
