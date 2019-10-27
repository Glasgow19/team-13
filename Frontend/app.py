#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 26 16:19:40 2019

@author: sarah
"""

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort,jsonify
import os
import twitter 
import gmail
import calUtils

app = Flask(__name__)

""" @app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"

@app.route('/login', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home() """

@app.route('/stats',methods=['GET'])
def stats():
    twitterInfo = twitter.getCalendar('jalfrazi_')
    gmailInfo = gmail.getLastSent()
    #print(twitterInfo)
    #print(gmailInfo)
    labels = calUtils.getMonthLabels()
    print(labels)
    print(twitterInfo)
    return render_template('stats.html',twitterInfo=twitterInfo[::-1],gmailInfo=gmailInfo[::-1])



if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
