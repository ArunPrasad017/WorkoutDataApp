import urllib


def authorize_url(CLIENT_ID):
    redirect_uri = "https://localhost.com/strava_auth_successful"
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": "activity:read_all",
    }
    values_url = urllib.parse.urlencode(params)
    base_url = "https://www.strava.com/oauth/authorize"
    return base_url + "?" + values_url
