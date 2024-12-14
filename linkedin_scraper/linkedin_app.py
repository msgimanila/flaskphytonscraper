from flask import Flask, request, redirect, session, url_for
import requests
from config import Config  # Import the config class

app = Flask(__name__)
app.config.from_object(Config)  # Load configurations from Config class
app.config.from_object('config.DevelopmentConfig')


# LinkedIn API endpoints
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
PROFILE_URL = 'https://api.linkedin.com/v2/me'
CONNECTIONS_URL = 'https://api.linkedin.com/v2/connections?q=viewer&projection=(elements*(to~))'

@app.route('/')
def index():
    return '<a href="/login">Login with LinkedIn</a>'

@app.route('/login')
def login():
    # Use configurations from the config file
    params = {
        'response_type': 'code',
        'client_id': app.config['LINKEDIN_CLIENT_ID'],
        'redirect_uri': app.config['LINKEDIN_REDIRECT_URI'],
        'scope': 'r_liteprofile r_emailaddress w_member_social'
    }
    auth_request = requests.Request('GET', AUTH_URL, params=params).prepare()
    return redirect(auth_request.url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return 'Error: No code provided', 400

    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': app.config['LINKEDIN_REDIRECT_URI'],
        'client_id': app.config['LINKEDIN_CLIENT_ID'],
        'client_secret': app.config['LINKEDIN_CLIENT_SECRET']
    }
    response = requests.post(TOKEN_URL, data=data)
    response_data = response.json()

    access_token = response_data.get('access_token')
    if not access_token:
        return 'Error: Unable to obtain access token', 400

    session['access_token'] = access_token
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(PROFILE_URL, headers=headers)
    profile_data = response.json()

    connections_response = requests.get(CONNECTIONS_URL, headers=headers)
    connections_data = connections_response.json()

    return f"""
        <h1>Profile Data</h1>
        <pre>{profile_data}</pre>
        <h1>Connections</h1>
        <pre>{connections_data}</pre>
    """

if __name__ == '__main__':
    app.run(debug=True)
