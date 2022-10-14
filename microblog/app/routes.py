from flask import (
    Blueprint,
    render_template,
)

router = Blueprint("router", __name__)


@router.route("/")
@router.route("/home")
def app_main():
    """
    Flask main function
    """
    return render_template("index.html")
