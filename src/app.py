import json

import requests
from flask import Flask, redirect, render_template, request, session, url_for

from src.auth import authorize_url, refresh_access_token
from src import strava_api
from src.config import *  # noqa

app = Flask(__name__)
app.secret_key = "teststring"

URL = "https://www.strava.com/api/v3/athlete/activities"
# Until v3 the url is going to be same so make as general config
# the final api call and method will be strongly coupled.

AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"

token_dict = {}
obj = strava_api.StravaApi(session=None)


@app.route("/")
@app.route("/home")
def app_main():
    """
    Flask main function
    """
    if not obj.session:
        obj.set_session(session)
        return render_template("index.html")

    return render_template("index.html", athlete_id=session["athlete_id"])


# Route for handling the login page logic
@app.route("/login", methods=["GET"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("login.html", error=error)


@app.route("/strava_authorize", methods=["GET"])
def strava_authorize():
    if "athlete_id" not in session or "refresh_token" not in session:
        return redirect(location=authorize_url(CLIENT_ID))
    return (
        "<html>"
        "<body>"
        "you are logged already "
        '<a href="http://localhost:5000/">go back</a>'
        "</body>"
        "</html>"
    )


@app.route("/strava_auth_successful")
def strava_auth_successful():
    print("Inside strava_auth_successful")
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code",
    }
    response = requests.post("https://www.strava.com/oauth/token", params=params)
    output_str = json.loads(response.content)
    ACCESS_TOKEN = output_str["access_token"]
    REFRESH_TOKEN = output_str["refresh_token"]

    token_dict[str(output_str["athlete"]["id"])] = [ACCESS_TOKEN, REFRESH_TOKEN]

    session["athlete_id"] = output_str["athlete"]["id"]
    session["refresh_token"] = output_str["refresh_token"]
    return redirect(url_for("app_main"))


@app.route("/strava_retreive_athlete")
def strava_retreive_athlete():
    athlete_id = obj.get_athlete_id()
    if athlete_id in token_dict:
        [ACCESS_TOKEN, REFRESH_TOKEN] = token_dict[athlete_id]
    else:
        if "refresh_token" not in session:
            return redirect(url_for("strava_authorize"))
        REFRESH_TOKEN = session["refresh_token"]
        # refresh access token here and assign
        token_dict[athlete_id] = [None, REFRESH_TOKEN]
    ACCESS_TOKEN = refresh_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response2 = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    print(f"{response2.json()=}")
    return render_template(
        "main.html",
        firstname=response2.json()["firstname"],
        lastname=response2.json()["lastname"],
    )
