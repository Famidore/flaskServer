from flask import send_from_directory
from flask_sqlalchemy import SQLAlchemy
from quart import Quart, render_template, websocket
from quart import Blueprint
import os
from src.pages.movies import get_movies_list
from src.pages.youtube import get_youtube_trending_videos
from src.pages.reddit import get_reddit_trends
from src.utils import obtain_key, threadReturn
from src.pages.wykop import get_wykop_trends


db = SQLAlchemy()

main = Blueprint("main", __name__)


yt_api_key = obtain_key(mode="youtube_key")


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


# @app.route("/pull", methods=["POST", "GET"])
# async def pull():
#     try:
#         subprocess.run(["git", "pull"], timeout=10, check=True)
#         subprocess.run(
#             ["pip", "install", "-r", "requirements.txt"], timeout=10, check=True
#         )
#         result = "Server update successfull!"
#     except subprocess.CalledProcessError as err:
#         result = f"Error during server update: {err.output.decode()}"
#         return render_template("pulling.html", result=result)

#     return await render_template("pulling.html", result=result)


@main.route("/trends", methods=["POST", "GET"])
async def trends():
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

    return await render_template(
        "trends.html",
        movies_list=zip(movies_list, movies_posters, movies_links),
        yt_data=zip(yt_titles, yt_imgs, yt_urls),
        reddit_trends=zip(rd_titles, rd_src, rd_link, rd_img, rd_descs),
        wykop_titles=zip(wykop_titles, wykop_imgs, wykop_links),
    )


@main.route("/reddit-inspect", methods=["POST", "GET"])
async def reddit_inspect():
    return await render_template("media/reddit_inspect.html")


@main.route("/wykop-inspect", methods=["POST", "GET"])
async def wykop_inspect():
    return await render_template("media/wykop_inspect.html")
