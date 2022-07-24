import os

import requests
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

from src.auth import authorize_url, refresh_access_token
from src import strava_api
from src.routes import router
from src.constants import *  # noqa

basedir = os.path.abspath(os.path.dirname(__file__))


# def create_app():
#     app = Flask(__name__)
#     app.secret_key = "teststring"
#     app.config.from_object("src.config.Config")
#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#         basedir, "database.db"
#     )
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#     db = SQLAlchemy(app)
#     return app, db


# app, db = create_app()
app = Flask(__name__)
app.secret_key = "teststring"
app.config.from_object("src.config.Config")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "../db/database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


URL = "https://www.strava.com/api/v3/athlete/activities"
# Until v3 the url is going to be same so make as general config
# the final api call and method will be strongly coupled.

AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"

token_dict = {}
obj = strava_api.StravaApi()
app.config["obj_to_pass"] = obj


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(400))
    refresh_token = db.Column(db.String(400))

    def __init__(self, user_id, user_name, refresh_token):
        self.user_id = user_id
        self.user_name = user_name
        self.refresh_token = refresh_token


# create a method of a class for this where all attributes such as obj
# can be one of input params to the class(routes.py is routing to the logic which needs
# to be a separate function)
# @app.route("/")
# @app.route("/home")
# def app_main():
#     """
#     Flask main function
#     """
#     if not obj.session:
#         obj.session = session
#         return render_template("index.html")

#     return render_template("index.html", athlete_id=obj.session["athlete_id"])

app.register_blueprint(router)


# Route for handling the login page logic
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("base.html", error=error)


@app.route("/strava_authorize", methods=["GET"])
def strava_authorize():
    if "athlete_id" not in obj.session or "refresh_token" not in obj.session:
        return redirect(location=authorize_url(CLIENT_ID))
    return (
        "<html>"
        "<body>"
        "you are logged already "
        '<a href="http://localhost:5000/">go back</a>'
        "</body>"
        "</html>"
    )


# remove/rewrite after discussion with Stefano
def set_refresh_token():
    obj.session["refresh_token"] = token_dict[obj.session["athlete_id"]][1]


# Changed global vars for db to an input param
def add_user_to_db(user, db):
    # TODO(Arun): add a check if the pk exists before making the update
    exists = db.session.query(
        db.session.query(User).filter_by(user_id=user.user_id).exists()
    ).scalar()
    if not exists:
        db.session.add(user)
        db.session.commit()


@app.route("/strava_auth_successful")
def strava_auth_successful():
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": request.args.get("code"),
        "grant_type": "authorization_code",
    }
    # add to the main strava api class(auth)
    token_dict[obj.session["athlete_id"]] = obj.get_access_refresh_token(params)
    set_refresh_token()
    return redirect(url_for("router.app_main"))


@app.route("/strava_retreive_athlete")
def strava_retreive_athlete():
    athlete_id = obj.get_athlete_id()
    if athlete_id in token_dict:
        [ACCESS_TOKEN, REFRESH_TOKEN] = token_dict[athlete_id]
    else:
        if "refresh_token" not in obj.session:
            return redirect(url_for("strava_authorize"))
        REFRESH_TOKEN = obj.session["refresh_token"]
        # refresh access token here and assign
        token_dict[athlete_id] = [None, REFRESH_TOKEN]
    ACCESS_TOKEN = refresh_access_token(REFRESH_TOKEN, CLIENT_ID, CLIENT_SECRET)
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response2 = requests.get("https://www.strava.com/api/v3/athlete", headers=headers)
    user = User(
        response2.json()["id"],
        response2.json()["username"],
        token_dict[response2.json()["id"]][1],
    )
    add_user_to_db(user, db)
    return render_template(
        "main.html",
        firstname=response2.json()["firstname"],
        lastname=response2.json()["lastname"],
    )
