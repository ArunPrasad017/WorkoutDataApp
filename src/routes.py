from flask import Blueprint, render_template, session, current_app

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
