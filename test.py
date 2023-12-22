from flask import Flask, render_template, send_from_directory, request
from datetime import datetime
import os
import subprocess
from movies import get_movies_list
from youtube import obtain_key, get_youtube_trending_videos

app = Flask(__name__)

api_key = obtain_key()


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "squid.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/time", methods=["GET", "POST"])
def time():
    return render_template("time.html")


@app.route("/pull", methods=["POST", "GET"])
def pull():
    try:
        subprocess.run(["git", "pull"], timeout=10, check=True)
        subprocess.run(
            ["pip", "install", "-r", "requirements.txt"], timeout=10, check=True
        )
        result = "Server update successfull!"
    except subprocess.CalledProcessError as err:
        result = f"Error during server update: {err.output.decode()}"
        return render_template("pulling.html", result=result)

    return render_template("pulling.html", result=result)


@app.route("/trends", methods=["POST", "GET"])
def trends():
    movies_list = []
    for i in get_movies_list():
        if (i.text) not in movies_list:
            movies_list.append(i.text)
    return render_template(
        "trends.html",
        movies_list=movies_list,
        yt_titles=get_youtube_trending_videos(api_key),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
