from quart import Blueprint, render_template
from dbs import *

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
async def login():
    return await render_template("login_forms/login.html")


@auth.route("/signup", methods=["POST", "GET"])
async def signup():
    return await render_template("login_forms/signup.html")


@auth.route("/logout", methods=["POST", "GET"])
async def logout():
    return await render_template("login_forms/login.html")
