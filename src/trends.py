from quart import render_template, Blueprint
from src.pages.movies import get_movies_list
from src.pages.youtube import get_youtube_trending_videos
from src.pages.reddit import get_reddit_trends
from src.utils import obtain_key, threadReturn
from src.pages.wykop import get_wykop_trends
from src.pages.posts_db.get_posts import get_posts

trending = Blueprint("trending", __name__)

yt_api_key = obtain_key(mode="youtube_key")


@trending.route("/trends", methods=["GET"])
async def trends():
    """
    youtube_name = "youtube"
    wykop_name = "wykop"
    filmweb_name = "filmweb"
    reddit_name = "reddit"

    t_yt = threadReturn(target=get_posts, args=(youtube_name,))
    t_rd = threadReturn(target=get_posts, args=(reddit_name,))
    t_wykop = threadReturn(target=get_posts, args=(wykop_name,))
    t_movies = threadReturn(target=get_posts, args=(filmweb_name,))

    t_yt.start()
    t_rd.start()
    t_wykop.start()
    t_movies.start()

    movies_list, movies_posters, movies_links = t_movies.join()
    yt_titles, yt_imgs, yt_urls = t_yt.join()
    rd_titles, rd_src, rd_link, rd_img, rd_descs = t_rd.join()
    wykop_titles, wykop_imgs, wykop_links = t_wykop.join()
    """
    movies_list, movies_posters, movies_links = get_posts("filmweb", 10)
    yt_titles, yt_imgs, yt_urls = get_posts("youtube", 10)
    rd_titles, rd_src, rd_link, rd_img, rd_descs = get_posts("reddit", 10)
    wykop_titles, wykop_imgs, wykop_links = get_posts("wykop", 10)

    return await render_template(
        "trends.html",
        movies_list=zip(movies_list, movies_posters, movies_links),
        yt_data=zip(yt_titles, yt_imgs, yt_urls),
        reddit_trends=zip(rd_titles, rd_src, rd_link, rd_img, rd_descs),
        wykop_titles=zip(wykop_titles, wykop_imgs, wykop_links),
    )


@trending.route("/reddit-inspect", methods=["POST", "GET"])
async def reddit_inspect():
    return await render_template("media/reddit_inspect.html")


@trending.route("/wykop-inspect", methods=["POST", "GET"])
async def wykop_inspect():
    return await render_template("media/wykop_inspect.html")
