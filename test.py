from flask import Flask, render_template, send_from_directory, request
from datetime import datetime
import os
import subprocess
from movies import get_movies_list
from youtube import get_youtube_trending_videos
from reddit import get_reddit_trends
from utils import obtain_key, threadReturn
from wykop import get_wykop_trends
import threading

app = Flask(__name__)

yt_api_key = obtain_key(mode="youtube_key")


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
    t_yt = threadReturn(target=get_youtube_trending_videos, args=(yt_api_key,))
    t_rd = threadReturn(target=get_reddit_trends)
    t_wykop = threadReturn(target=get_wykop_trends)
    t_movies = threadReturn(target=get_movies_list)

    t_yt.start()
    t_rd.start()
    t_wykop.start()
    t_movies.start()

    movies_list, movies_posters, movies_links = t_movies.join()
    yt_titles, yt_imgs, yt_urls = t_yt.join()
    rd_titles, rd_src, rd_link, rd_img, rd_descs = t_rd.join()
    wykop_titles, wykop_imgs, wykop_links = t_wykop.join()

    return render_template(
        "trends.html",
        movies_list=zip(movies_list, movies_posters, movies_links),
        yt_data=zip(yt_titles, yt_imgs, yt_urls),
        reddit_trends=zip(rd_titles, rd_src, rd_link, rd_img, rd_descs),
        wykop_titles=zip(wykop_titles, wykop_imgs, wykop_links),
    )


@app.route("/reddit-inspect", methods=["POST", "GET"])
def reddit_inspect():
    return render_template("reddit_inspect.html")


@app.route("/wykop-inspect", methods=["POST", "GET"])
def wykop_inspect():
    return render_template("wykop_inspect.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
