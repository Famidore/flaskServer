from flask import send_from_directory
from quart import render_template
from quart import Blueprint
import os


main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
async def index():
    return await render_template("index.html")


@main.route("/favicon.ico")
async def favicon():
    return await send_from_directory(
        os.path.join(main.root_path, "static"),
        "squid.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@main.route("/time", methods=["GET", "POST"])
async def time():
    return await render_template("time.html")
