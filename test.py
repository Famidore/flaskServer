from flask import Flask, render_template, send_from_directory, request
from datetime import datetime
import os
import subprocess
from movies import get_movies_list
from youtube import obtain_key, get_youtube_trending_videos
from reddit import get_reddit_trends

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
    movies_list, movies_posters, movies_links = get_movies_list()
    yt_titles, yt_imgs, yt_urls = get_youtube_trending_videos(api_key)
    rd_titles, rd_src, rd_link, rd_img = get_reddit_trends()

    return render_template(
        "trends.html",
        movies_list=zip(movies_list, movies_posters, movies_links),
        yt_data=zip(yt_titles, yt_imgs, yt_urls),
        reddit_trends=zip(rd_titles, rd_src, rd_link, rd_img),
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
