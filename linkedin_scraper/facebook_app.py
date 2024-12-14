from flask import Flask, redirect, request, session, url_for
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Facebook API Endpoints
AUTH_URL = 'https://www.facebook.com/v13.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v13.0/oauth/access_token'
PROFILE_URL = 'https://graph.facebook.com/me'

@app.route('/')
def index():
    return '<a href="/facebook/login">Login with Facebook</a>'

@app.route('/facebook/login')
def facebook_login():
    params = {
        'client_id': app.config['FACEBOOK_CLIENT_ID'],
        'redirect_uri': app.config['FACEBOOK_REDIRECT_URI'],
        'scope': 'email,public_profile',
        'response_type': 'code',
    }
    auth_request = requests.Request('GET', AUTH_URL, params=params).prepare()
    return redirect(auth_request.url)

@app.route('/facebook/callback')
def facebook_callback():
    code = request.args.get('code')
    if not code:
        return 'Error: No code provided', 400

    data = {
        'client_id': app.config['FACEBOOK_CLIENT_ID'],
        'client_secret': app.config['FACEBOOK_CLIENT_SECRET'],
        'redirect_uri': app.config['FACEBOOK_REDIRECT_URI'],
        'code': code,
    }
    response = requests.get(TOKEN_URL, params=data)
    response_data = response.json()

    access_token = response_data.get('access_token')
    if not access_token:
        return 'Error: Unable to obtain access token', 400

    session['access_token'] = access_token
    return redirect(url_for('facebook_profile'))

@app.route('/facebook/profile')
def facebook_profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('facebook_login'))

    params = {'access_token': access_token}
    response = requests.get(PROFILE_URL, params=params)
    profile_data = response.json()

    return f"""
        <h1>Facebook Profile Data</h1>
        <pre>{profile_data}</pre>
    """

if __name__ == '__main__':
    app.run(debug=True)
