from quart import Blueprint, render_template, redirect, url_for
from quart_auth import (
    current_user,
    login_required,
    Unauthorized,
)

user_profile = Blueprint("profile", __name__)


@user_profile.route("/profile", methods=["POST", "GET"])
@login_required
async def profile():
    return await render_template("login_forms/profile.html", user=current_user.auth_id)


@user_profile.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    """
    zrobić podstronę informującą o braku dostępu i z możliwością przekierowania do loginu/rejestracji
    """
    return redirect(url_for("auth.login"))
