from quart import Blueprint, render_template, request, redirect, url_for
from quart_auth import (
    AuthUser,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from secrets import compare_digest
from src.utils import obtain_key

auth = Blueprint("auth", __name__)


@auth.route("/login", methods={"GET", "POST"})
async def login():
    """
    Check credentials (username && password)
    """

    username = obtain_key(mode="db_username")
    password = obtain_key(mode="db_password")

    if request.method == "POST":
        data = await request.form
        if data["email"] == username and compare_digest(data["password"], password):
            login_user(AuthUser(username))  # user ID from dbs
            return redirect(url_for("profile.profile"))
        else:
            return "lol"

    return await render_template("login_forms/login.html")


@auth.route("/signup")
async def signup():
    return current_user.auth_id or "you are not logged in"
    # return await render_template("login_forms/signup.html")


@auth.route("/logout")
async def logout():
    logout_user()
    return redirect(url_for("auth.login"))
