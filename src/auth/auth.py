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
from src.auth.auth_db.auth_db import register_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods={"GET", "POST"})
async def login():
    """
    Check credentials (username && password)
    """

    username = obtain_key(mode="db_username")
    password = obtain_key(mode="db_password")
    role = obtain_key(mode="role")

    if request.method == "POST":
        data = await request.form
        if data["email"] == username and compare_digest(data["password"], password):
            if role == "admin":
                login_user(AuthUser("ADMIN"))  # user ID from dbs
            else:
                login_user(AuthUser("USER"))
            return redirect(url_for("profile"))
        else:
            return await render_template("login_forms/signup.html",
                                         message="Invalid username or password")

    return await render_template("login_forms/profile.html")


@auth.route("/signup")
async def signup():
    # return current_user.auth_id or "you are not logged in"
    return await render_template("login_forms/signup.html")


@auth.route("/register", methods={"POST"})
async def register():
    data=await request.form
    name=data["name"]
    email=data["email"]
    password=data["password"]
    register_message:str
    if name is not None and email is not None and password is not None:
        register_message=register_user(name, email, password)
    else:
        register_message="Error: Arguments did not received!"
    return await render_template("login_forms/signup_response.html", message=register_message)


@auth.route("/logout")
async def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/unauthorized")
async def unauthorized():
    return await render_template("login_forms/unauthorized.html")
