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
    access = flask.session['auth_token']['access_token']
    cal.main(access)
    s, e = cal.create_calendar_matrix()

    twitterInfo = twitter.getCalendar('jalfrazi_')
    userId = google_auth.get_user_info()['id']
    
    gmailInfo = gmail.getLastSent(access,userId)

    return render_template('dashboard.html', slots=s, events=e, twitterInfo=twitterInfo[::-1], gmailInfo=gmailInfo[::-1])


@app.route('/questionnaire')
def questionnaire():
    return render_template('questionnaire.html')


@app.route('/')
def index():
    if google_auth.is_logged_in():
        print(flask.session)
        userInfo = google_auth.get_user_info()
        return render_template('list.html',user_info=userInfo)
    else:
        return redirect('/google/login')

    return 'You are not currently logged in.'
