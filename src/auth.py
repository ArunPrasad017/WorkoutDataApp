import urllib


AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"


def authorize_url(CLIENT_ID):
    redirect_uri = "https://127.0.0.1:5000/strava_auth_successful"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "activity:read_all",
    }
    values_url = urllib.parse.urlencode(params)
    return AUTHORIZATION_BASE_URL + "?" + values_url
