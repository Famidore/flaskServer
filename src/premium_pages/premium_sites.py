from quart import render_template, Blueprint, redirect, url_for
from quart_auth import login_required, current_user, Unauthorized
from src.premium_pages.premium_scrapers.movies_premium import get_movies_premium
from src.premium_pages.premium_scrapers.reddit_premium import get_reddit_premium
from src.premium_pages.premium_scrapers.wykop_premium import get_wykop_premium
from src.premium_pages.premium_scrapers.yt_premium import get_youtube_premium_objects
from src.utils import obtain_key, threadReturn

premium = Blueprint("premium", __name__, url_prefix="/trends")
yt_api_key = obtain_key(mode="youtube_key")


@premium.route("/hub", methods=["POST", "GET"])
@login_required
async def premium_main():
    return await render_template("premium/premium_hub.html")


@premium.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    """
    Powiadom że nie ma dostępu!
    """
    return redirect(url_for("auth.login"))