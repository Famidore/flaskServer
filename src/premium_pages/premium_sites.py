from quart import render_template, Blueprint, redirect, url_for, request
from quart_auth import login_required, Unauthorized
from src.premium_pages.premium_scrapers.movies_premium import get_movies_premium
from src.premium_pages.premium_scrapers.reddit_premium import get_reddit_premium
from src.premium_pages.premium_scrapers.wykop_premium import get_wykop_premium
from src.premium_pages.premium_scrapers.yt_premium import get_youtube_premium_objects
from src.utils import obtain_key, threadReturn
from src.premium_pages.premium_scrapers.get_categories import get_categories

premium = Blueprint("premium", __name__, url_prefix="/trends")
yt_api_key = obtain_key(mode="youtube_key")


@premium.route("/hub")
@login_required
async def premium_main():
    return await render_template("premium/premium_hub.html")


@premium.route("/hub/configure", methods=["POST"])
@login_required
async def premium_config():
    userCategories = obtain_key(
        "src/premium_pages/premium_scrapers/tempCategories.json", reneder_whole=True
    )

    if request.method == "POST":
        data_form = await request.form
        if list(data_form.to_dict().keys())[0] == "user_category_list":
            data = list(data_form.to_dict().values())[0]
            if data in userCategories[1][0]:
                print(data)
                # modify dbs
            else:
                print("field not in dataset")
        elif list(data_form.to_dict().keys())[0] == "category_list":
            data = list(data_form.to_dict().values())[0]
            print("category_list")
            # add to user categories dbs

    return await render_template(
        "premium/premium_config.html",
        allCategories=get_categories(10),
        userCategories=userCategories,
    )


@premium.errorhandler(Unauthorized)
async def redirect_to_login(*_):
    return redirect(url_for("auth.unauthorized"))
