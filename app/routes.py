from flask import Flask, request, redirect, render_template, session, url_for
from auth import request_access_token, user_authorization
import os, time, requests, base64
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
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
    auth_url = user_authorization()
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
    
    code = request.args.get('code')
    
    response = request_access_token(code)
    # session["token_info"] = response
    # response = session['token_info']
    if 'error' in response:
        # noticed that when this page reloads, the response has an error
        # in the body
        # this condition is meant to refresh the page and get new access_tokens
        # for when the user refreshes the page
        return redirect(url_for('login'))
    
    # get user's token
    token = response.get('access_token')
    
    # spotify uri to request current user info
    url = "https://api.spotify.com/v1/me"
    headers = {
        'Authorization' : 'Bearer ' + token
    }
    user_response = requests.get(url, headers=headers)
    
    # parse user's info to get display_name
    u_response = user_response.json()
    user_name = u_response['display_name'] 
    
    # store access information in session
    session[user_name] = response

    # reirect user to their page    
    return redirect(f'/{user_name}')


@app.route("/<user>", strict_slashes=False)
def user_page(user):
    """
    user's page
    """
   
    
    return render_template('index.html', user=user)


@app.route("/logout")
def logout():
    user_name = request.args.get("user")
    session.pop(user_name, None)
    return redirect(url_for("home"))


def get_access_token(token_info):
    """
    get token or refresh token if expired
    """
    
    if "access_info" not in session:
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
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
