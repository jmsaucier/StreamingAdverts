from datetime import datetime
from flask import render_template, session
from app import app
from oauth import OAuthSignIn
from pymongo import MongoClient
from bson import json_util
import json

from marketingroutes import *

@app.route('/')
@app.route('/home')
def home():
    
    if( not 'isAnonymous' in session):
        if('oauth_access_token' in session and session['oauth_access_token'] != ''):
            session['isAnonymous'] = False
        else:
            session['isAnonymous'] = True

    return render_template(
        'index.jade',
        title = 'Home Page',
        year = datetime.now().year,
    )

@app.route('/callback')
def callback():
    auth = OAuthSignIn(app)
    return auth.callback()


@app.route('/broadcasting')
def broadcasting():
    pass

@app.route('/authorize')
def authorize():
    auth = OAuthSignIn(app)
    return auth.authorize('user_read')

@app.route('/contact')
def contact():
    return render_template(
        'contact.jade',
        title = 'Contact',
        year = datetime.now().year,
        message = 'Your contact page.'
    )

@app.route('/about')
def about():
    return render_template(
        'about.jade',
        title = 'About',
        year = datetime.now().year,
        message = 'Your application description page.'
    )

@app.route('/logout')
def logout():
    session['isAnonymous'] = True
