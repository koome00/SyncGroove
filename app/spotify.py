import os
from dotenv import load_dotenv
import requests
import base64
import time

# Allow loading environment variables from .env file
load_dotenv()


c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv("CLIENT_SECRET")
r_uri = 'http://localhost:5000/home/'

def user_authorization():
    """
    request user authorization
    """
    # scope are permisions given by user
    scope = 'user-read-private user-read-email user-top-read playlist-read-private user-read-currently-playing'
    
    # authorization url
    OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'

    # create query for authorization code flow check documentation
    # https://developer.spotify.com/documentation/web-api/tutorials/code-flow
    q = f"client_id={c_id}&response_type=code&redirect_uri={r_uri}&scope={scope}"
    
    # authorization url to be used by GET method
    authorization_url = f"{OAUTH_AUTHORIZE_URL}?{q}"    

    return authorization_url

def request_access_token(authorization_code):
    """
    requests access token after user has given authorization
    this function makes a post requests given the the required header
    and data parameters 
    """
    # endpoint to make post request
    OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'

    # encode client_id and secret_id in base64
    auth = c_id + ":" + c_secret
    auth_string = auth.encode('utf-8')
    auth64 = str(base64.b64encode(auth_string), 'utf-8')
    
    # body parameters
    # code is retrived from the redirect_uri query paramaters
    # and given to body
    data = {"grant_type": "authorization_code",
            "code": authorization_code,
            "redirect_uri": r_uri,
            }
    
    # header for the POST request
    headers = {"Authorization": "Basic " + auth64,
               "Content-type": "application/x-www-form-urlencoded"}
    
    # make post request
    response = requests.post(OAUTH_TOKEN_URL, headers=headers, data=data)

    # get response body and parse it using .json()
    response_data = response.json()
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    expires_in = response_data["expires_in"]

    expires_at = int(time.time()) + expires_in
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return response_data, auth_header, refresh_token, expires_at


def get_refresh_token(refresh_token):
    
    auth = c_id + ":" + c_secret
    auth_string = auth.encode('utf-8')
    auth64 = str(base64.b64encode(auth_string), 'utf-8')
    body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    headers = {
        'content-Type': 'application/x-www-form-urlencoded',
        'Authorization': "Basic " + auth64
    }
    
    url = "https://accounts.spotify.com/api/token"
    post_refresh = requests.post(url, data=body, headers=headers)
    response_data = post_refresh.json()
    access_token = response_data["access_token"]
    expires_in = response_data["expires_in"]
    expires_at = int(time.time()) + expires_in

    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    return auth_header, expires_at

def check_expired(expired_at):
    now = int(time.time())
    if expired_at - now <= 0:
        return True
    return False


def current_user_profile(auth_header):

    url = "https://api.spotify.com/v1/me"

    response = requests.get(url, headers=auth_header)
    r = response.json()
    name = r['display_name']
    followers = r['followers']['total']
    p_pic = r['images'][0]['url']
    return name, followers, p_pic

def current_user_playlists(auth_header):
    url = "https://api.spotify.com/v1/me/playlists?limit=50"

    
    response = requests.get(url, headers=auth_header)

    return response.json()

def currently_playing(auth_header):
    url = "https://api.spotify.com/v1/me/player/currently-playing"

    response = requests.get(url, headers=auth_header)
    r = response.json()
    name = r['device']['name']
    song = r['item']['name']
    artist = r['item']['artists']['name']
    
    return name, song, artist

def get_featured_playlists(auth_header):
    url = "https://api.spotify.com/v1/browse/featured-playlists?limit=50"
    response = requests.get(url, headers=auth_header)
    return response.json()
    
