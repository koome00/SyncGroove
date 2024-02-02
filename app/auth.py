import os
from dotenv import load_dotenv
import requests
import base64

# Allow loading environment variables from .env file
load_dotenv()


c_id = os.getenv('CLIENT_ID')
c_secret = os.getenv("CLIENT_SECRET")
r_uri = 'http://192.168.0.14:5000/home/'

def user_authorization():
    """
    request user authorization
    """
    # scope are permisions given by user
    scope = 'user-read-private user-read-email'
    
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
    r = response.json()

    # the json body will have the following key:value
    # access_token(str), token_type(str), scope(str)
    # expires_in(int), and refresh_token(str)
    # use r.get('access_token')
    return r
