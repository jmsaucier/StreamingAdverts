from flask import session, request, redirect, url_for
import requests
import urllib
import twitchapiretriever
import random
import string
from pymongo import MongoClient

class OAuthSignIn:
    def __init__(self, app):
        self.client_id = app.config['OAuth_ClientID']
        self.client_secret = app.config['OAuth_ClientSecret']
        self.authorize_url = app.config['OAuth_RedirectUrl']
        self.access_token_url = app.config['OAuth_PostUrl']

    def generateRandomUsername(self):
        return str(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15)))

    def get_authorize_url(self, scope=None, response_type=None, redirect_uri=None):
        url = self.authorize_url
        if scope or response_type or redirect_uri:
            url += "?"
            url += "client_id=" + self.client_id
            if scope:
                url += "&"
                url += "scope=" + scope

            if response_type:
                url += "&"
                url += "response_type=" + response_type

            if redirect_uri:
                url += "&"
                url += "redirect_uri=" + urllib.quote_plus(redirect_uri)
        return url


    def authorize(self, auth_scope):
        url = ''
        try:
            url = self.get_authorize_url(response_type='code', scope=auth_scope, redirect_uri=self.get_callback_url())
        except Exception as e:
            print e

        return redirect(url)



    def callback(self):
        if not 'code' in request.args:
            return redirect(url_for('error'))

        try:
            session['oauth_access_token'] = twitchapiretriever.getAccessToken(self.client_id, self.client_secret, request.args['code'], self.get_callback_url())
        except Exception as e:
            print e
        userInfo = twitchapiretriever.getUserInformation(self.client_id, session['oauth_access_token'])

        def log_access_token(username, access_token, scope):
            client = MongoClient() 
            db = client.ads
            collection = db.access_tokens
            collection.update({
                    "username":username
                },
                {
                    "username": username,
                    "access_token":access_token, 
                    "scope":scope
                }, 
                True)

        session['username'] = userInfo['name']

        #session['isAnonymous'] = False
        try:
            if('scope' in request.args):
                log_access_token(session['username'], session['oauth_access_token'], request.args['scope'].split('+'))
        except:
            pass
        return redirect(url_for('home'))

    def get_callback_url(self):
        return url_for('callback', _external=True)
