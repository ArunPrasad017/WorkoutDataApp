import urllib

import requests


AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"
REFRESH_ACCESS_TOKEN_URL = "https://www.strava.com/api/v3/oauth/token"


def authorize_url(CLIENT_ID):
    redirect_uri = "http://localhost:5000/strava_auth_successful"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "activity:read_all",
    }
    values_url = urllib.parse.urlencode(params)
    return f"{AUTHORIZATION_BASE_URL}?{values_url}"


def refresh_access_token(refresh_token, CLIENT_ID, CLIENT_SECRET):
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    refreshed_token = requests.post(REFRESH_ACCESS_TOKEN_URL, params=params).json()
    return refreshed_token["access_token"]
