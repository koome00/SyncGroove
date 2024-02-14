@app.route("/profile", strict_slashes=False)
def profile():
    """
    user's profile page
    """
    check_state()
    name, followers, p_pic, user_uri = spotify.current_user_profile(session['auth_header'])
    session['user_uri'] = user_uri
    playlists = spotify.current_user_playlists(session['auth_header'])
    return render_template('index.html',
                           name=name,
                           followers=followers,
                           p_pic=p_pic,
                           playlists=playlists["items"])