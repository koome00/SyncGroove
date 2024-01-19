from flask import Flask, request, url_for, redirect, render_template
from auth import request_access_token, user_authorization


app = Flask(__name__)

TOKEN_INFO = {}

@app.route("/", strict_slashes=False)
def home():
    
    return render_template('index.html')


@app.route("/login", strict_slashes=False)
def authorize():
    """
    redirects user to spotify to give authorization
    """
    auth_url = user_authorization()
    return redirect(auth_url) 

@app.route("/callback", strict_slashes=False)
def authorized():
    """
    if user gives permission, they will be redirected here
    the code parameter is extracted to get token information
    """
    # if auth is granted, take code and use the request_access_token 
    # to be given access token info
    # ...not yet completed...
    code = request.args.get('code')
    token_info = request_access_token(code)
    TOKEN_INFO.update(token_info)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
