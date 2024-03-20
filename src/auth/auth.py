from quart import Blueprint, render_template

# from dbs import logindb

auth = Blueprint("auth", __name__)


@auth.route("/login")
async def login():
    return await render_template("login_forms/login.html")


@auth.route("/signup")
async def signup():
    return await render_template("login_forms/login.html")


@auth.route("/logout")
async def logout():
    return await render_template("login_forms/login.html")
