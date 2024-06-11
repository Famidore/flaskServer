from quart import Blueprint, render_template, redirect, url_for, request
from quart_auth import (
    current_user,
    login_required,
    Unauthorized,
)
from src.auth.auth_db.auth_db import user_upgrade

user_profile = Blueprint("profile", __name__)


@user_profile.route("/profile", methods=["POST", "GET"])
@login_required
async def profile():
    if request.method == "POST":
        user_upgrade(current_user.auth_id)
        print(current_user.auth_id + " upgraded to premium")
    return await render_template("login_forms/profile.html", user=current_user.auth_id)


@user_profile.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    return redirect(url_for("auth.unauthorized"))
