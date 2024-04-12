from quart import render_template, Blueprint
from src.premium_pages.premium_scrapers.movies_premium import get_movies_premium
from src.premium_pages.premium_scrapers.reddit_premium import get_reddit_premium
from src.premium_pages.premium_scrapers.wykop_premium import get_wykop_premium
from src.premium_pages.premium_scrapers.yt_premium import get_youtube_premium_objects
from src.utils import obtain_key, threadReturn

premium = Blueprint("premium", __name__)
yt_api_key = obtain_key(mode="youtube_key")
