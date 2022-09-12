from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from src.auth import authorize_url

router = Blueprint("router", __name__)


@router.route("/")
@router.route("/home")
def app_main():
    """
    Flask main function
    """
    obj = current_app.config["obj_to_pass"]
    if not obj.session:
        obj.session = session
        return render_template("index.html")

    return render_template("index.html", athlete_id=obj.session["athlete_id"])


# Route for handling the login page logic
@router.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != "admin" or request.form["password"] != "admin":
            error = "Invalid Credentials. Please try again."
        else:
            return redirect(url_for("home"))
    return render_template("base.html", error=error)