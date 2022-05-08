import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy

from src.auth import authorize_url, refresh_access_token
from src import strava_api
from src.constants import *  # noqa

app = Flask(__name__)
app.secret_key = "teststring"
app.config.from_object("src.config.Config")
db = SQLAlchemy(app)


URL = "https://www.strava.com/api/v3/athlete/activities"
# Until v3 the url is going to be same so make as general config
# the final api call and method will be strongly coupled.

AUTHORIZATION_BASE_URL = "https://www.strava.com/oauth/authorize"

token_dict = {}
obj = strava_api.StravaApi()


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(400))
    refresh_token = db.Column(db.String(400))

    def __init__(self, id, user_name, refresh_token):
        self.id = id
        self.user_name = user_name
        self.refresh_token = refresh_token


class AuthTypeDim(db.Model):
    __tablename__ = "auth_type_dim"
    type_id = db.Column(db.Integer, primary_key=True)
    type_name = db.Column(db.String(400))

    def __init__(self, type_id, type_name):
        self.type_id = type_id
        self.type_name = type_name


class UserAuthType(db.Model):
    __tablename__ = "user_auth_type"
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True, nullable=False
    )
    user = db.relationship("User")
    auth_type_id = db.Column(
        db.Integer,
        db.ForeignKey("auth_type_dim.type_id"),
        primary_key=True,
        nullable=False,
    )
    auth_relation = db.relationship("AuthTypeDim")


@app.route("/")
@app.route("/home")
def app_main():
    """
    Flask main function
    """
    if not obj.session:
        obj.session = session
        return render_template("index.html")

    return render_template("index.html", athlete_id=obj.session["athlete_id"])


# Route for handling the login page logic
@app.route("/login", methods=["GET"])
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


def add_user_to_db(user):
    # TODO(Arun): add a check if the pk exists before making the update
    print(user)
    exists = db.session.query(
        db.session.query(User).filter_by(id=user.id).exists()
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
    response2 = requests.get(
        "https://www.strava.com/api/v3/athlete",
        headers={"Authorization": f'Bearer {token_dict[obj.session["athlete_id"]][0]}'},
    )
    print(response2.json())
    user = User(
        response2.json()["id"],
        response2.json()["username"],
        token_dict[response2.json()["id"]][1],
    )
    add_user_to_db(user)
    return redirect(url_for("app_main"))


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

    return render_template(
        "main.html",
        firstname=response2.json()["firstname"],
        lastname=response2.json()["lastname"],
    )
