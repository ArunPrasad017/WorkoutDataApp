import json

import requests
from flask import Flask, redirect, render_template, request, session, url_for

from auth import authorize_url, refresh_access_token

app = Flask(__name__)
app.secret_key = "teststring"

URL = "https://www.strava.com/api/v3/athlete/activities"
# Until v3 the url is going to be same so make as general config
# the final api call and method will be strongly coupled.

AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"
CLIENT_ID = ""
CLIENT_SECRET = ""
token_dict = {}


@app.route("/")
def app_main():
    """
    Flask main function
    """
    return render_template("index.html")


# Route for handling the login page logic
@app.route("/login", methods=["GET"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or \
                request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/strava_authorize", methods=["GET"])
def strava_authorize():
    breakpoint()
    if "athlete_id" not in session:
        return redirect(location=authorize_url(CLIENT_ID))
    print(session)
    return render_template("index.html")


@app.route("/strava_auth_successful")
def strava_auth_successful():
    print("Inside strava_auth_successful")
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code"
    }
    response = requests.post(
        "https://www.strava.com/oauth/token", params=params)
    print(f"Content: {response.content}")
    output_str = json.loads(response.content)
    ACCESS_TOKEN = output_str['access_token']
    REFRESH_TOKEN = output_str['refresh_token']
    token_dict[str(output_str['athlete']['id'])] = [
        ACCESS_TOKEN, REFRESH_TOKEN]

    session["athlete_id"] = output_str['athlete']['id']
    session["refresh_token"] = REFRESH_TOKEN
    return redirect(url_for('home'))


@app.route("/strava_retreive_athlete")
def strava_retreive_athlete():
    print(token_dict)
    if "athlete_id" in token_dict:
        [ACCESS_TOKEN, REFRESH_TOKEN] = (token_dict["athlete_id"])
    else:
        REFRESH_TOKEN = session["refresh_token"]
        # refresh access token here and assign
        token_dict[session["athlete_id"]] = [None, REFRESH_TOKEN]
    ACCESS_TOKEN = refresh_access_token(
        REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    params = {
        "Authorization": f'Bearer {ACCESS_TOKEN}'
    }
    response2 = requests.get(
        "https://www.strava.com/api/v3/athlete", params=params)
    print(f"{response2.text=}")


@app.route("/home")
def home():
    return render_template("index.html")
