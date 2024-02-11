from flask import Flask, request, redirect, jsonify, render_template, session, url_for
from flask_cors import CORS
import spotify
import os, time, requests, base64
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv
import json

load_dotenv()
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')
app.permanent_session_lifetime = timedelta(days=1)
c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv("CLIENT_SECRET")

  
@app.route("/", strict_slashes=False)
def home():
    """
    route handling the login page
    """
    return render_template('home.html')


@app.route("/login", strict_slashes=False)
def login():
    """
    redirects user to spotify to give authorization
    code used to get access token is in the redirect uri paramaters
    """
    auth_url = spotify.user_authorization()
    return redirect(auth_url) 


@app.route("/home/", strict_slashes=False)
def authorized():
    """
    if user gives permission, they will be redirected here
    the code parameter is extracted to get token information
    The user is then redirected to the home page after their code is captured
    and stored in their session
    """
    # if auth is granted, take code and use the request_access_token 
    # to be given access token info
    # ...not yet completed...
    session.clear()
    code = request.args.get('code')
    response, auth_header, refresh_token, expires_at = spotify.request_access_token(code)
    session['auth_header'] = auth_header
    session['refresh_token'] = refresh_token
    session['expires_at'] = expires_at
    # session["token_info"] = response
    # response = session['token_info']
    if 'error' in response:
        # noticed that when this page reloads, the response has an error
        # in the body
        # this condition is meant to refresh the page and get new access_tokens
        # for when the user refreshes the page
        return redirect(url_for('login'))
        
       
    return redirect(url_for('profile'))


@app.route("/profile", strict_slashes=False)
def profile():
    """
    user's profile page
    """
    check_state()
    name, followers, p_pic = spotify.current_user_profile(session['auth_header'])
    playlists = spotify.current_user_playlists(session['auth_header'])
    return render_template('index.html',
                           name=name,
                           followers=followers,
                           p_pic=p_pic,
                           playlists=playlists["items"])
    

    

@app.route("/logout")
def logout():
    user_name = request.args.get("user")
    session.pop(user_name, None)
    return redirect(url_for("home"))


def check_state():
    state = spotify.check_expired(session['expires_at'])
    if state is True:
        auth_header, expires_at = spotify.get_refresh_token(session['refresh_token'])
        session['auth_header'] = auth_header
        session['expires_at'] = expires_at


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
