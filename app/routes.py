from flask import Flask, request, redirect, render_template, session, url_for
from auth import request_access_token, user_authorization
import os
import time
import requests
import base64


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv("CLIENT_SECRET")
TOKEN_INFO = 'token_info'
  
@app.route("/", strict_slashes=False)
def home():
    
    return render_template('home.html')


@app.route("/login", strict_slashes=False)
def login():
    """
    redirects user to spotify to give authorization
    """
    auth_url = user_authorization()
    return redirect(auth_url) 

@app.route("/home", strict_slashes=False)
def authorized():
    """
    if user gives permission, they will be redirected here
    the code parameter is extracted to get token information
    """
    # if auth is granted, take code and use the request_access_token 
    # to be given access token info
    # ...not yet completed...
    code = request.args.get('code')
    session.clear()
    token_info = request_access_token(code)
    
    access_token = get_access_token(token_info)
    return render_template('index.html', access_token=access_token)

def get_access_token(token_info):
    """
    get token or refresh token if expired
    """
    session[TOKEN_INFO] = token_info
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        # if the token info is not found, redirect the user to the login route
        redirect(url_for('login'))
    
    # check if the token is expired and refresh it if necessary
    now = int(time.time())

    is_expired = token_info.get('expires_in') - now < 3600
    

    if is_expired:
        url = 'https://accounts.spotify.com/api/token'
        # encode client_id and secret_id in base64
        auth = c_id + ":" + c_secret
        auth_string = auth.encode('utf-8')
        auth64 = str(base64.b64encode(auth_string), 'utf-8')

        data = {"grant_type": "refresh_token",
            "refresh_token": token_info['refresh_token']
            }
        
        # header for the POST request
        headers = {"Authorization": "Basic " + auth64,
               "Content-type": "application/x-www-form-urlencoded"}
        # make post request
        response = requests.post(url, headers=headers, data=data)

        token_info = response.json()
        session[TOKEN_INFO] = token_info
    
    return token_info.get('access_token')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
