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
from src.auth.auth_db.auth_db import register_user, check_user_credencials
from src.auth.auth_db.auth_db import login_user as login_database


auth = Blueprint("auth", __name__)


@auth.route("/login", methods={"GET", "POST"})
async def login():

    if request.method == "POST":
        data = await request.form
        if data["name"] == obtain_key(mode="admin_username") and data[
            "password"
        ] == obtain_key(mode="admin_password"):
            login_user(AuthUser("ADMIN"))
        elif login_database(data["name"], data["password"]):
            login_user(AuthUser(data["name"]))
            return redirect(url_for("profile.profile"))
        else:
            return await render_template("login_forms/login.html")

    return await render_template("login_forms/login.html")


@auth.route("/signup", methods={"GET", "POST"})
async def signup():
    if request.method == "POST":
        data = await request.form
        register_user(data["name"], data["email"], data["password"])
        login_user(AuthUser(data["name"]))
        return redirect(url_for("profile.profile"))
    return await render_template("login_forms/signup.html")


@auth.route("/register")
async def register():
    return await render_template("login_forms/signup_succed.html")


@auth.route("/logout")
async def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/unauthorized")
async def unauthorized():
    return await render_template("login_forms/unauthorized.html")
