import requests
from flask import Flask, redirect, render_template, request, url_for

# from authlib.integrations.requests_client import OAuth2Session
from auth import authorize_url


app = Flask(__name__)

ACCESS_TOKEN = ""
URL = "https://www.strava.com/api/v3/athlete/activities"
# Until v3 the url is going to be same so make as general config
# the final api call and method will be strongly coupled.

AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"
CLIENT_ID = ""
CLIENT_SECRET = ""


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
    return redirect(location=authorize_url(CLIENT_ID))


@app.route("/strava_auth_successful", methods=["GET"])
def strava_auth_successful():
    # params = {
    #     "client_id": CLIENT_ID,
    #     "client_secret": CLIENT_SECRET,
    #     "code": "test",
    #     "grant_type": "authorization_code"
    # }
    print(request.args.get("code"))
    print(request.args.get("scope"))


@app.route("/home")
def home_page():
    return "Done"


def return_resp():
    """
    Temp function
    """
    headers_auth = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    print(headers_auth)
    response = requests.get(URL, headers=headers_auth)
    return response.content


# oauth separate module as a plain python method, called as part of main
# and does only oauth
