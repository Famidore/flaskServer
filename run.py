import quart_flask_patch
from quart import Quart
from quart_auth import QuartAuth
from werkzeug.local import LocalProxy
from src.pages.posts_db.models import db
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.pages.posts_db.adding_posts import (
    add_wykop_to_db,
    add_movies_to_db,
    add_youtube_to_db,
    add_reddit_to_db,
    initialize_platforms,
)
from src.utils import obtain_key


def setup_app():
    app = Quart(__name__)
    app.config["SECRET_KEY"] = obtain_key(mode="app_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = obtain_key(
        file_path="CONFIG.json", mode="database_url"
    )
    db.init_app(app)
    QuartAuth(app)

    from src.auth.auth import auth as auth_blueprint
    from main import main as main_blueprint
    from src.trends import trending as trending_blueprint
    from src.premium_pages.premium_sites import premium as premium_blueprint
    from src.user_profile.profile import user_profile as profile_blueprint
    from src.admin_hub.admin_index import admin_hub as admin_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(trending_blueprint)
    app.register_blueprint(premium_blueprint)
    app.register_blueprint(profile_blueprint)
    app.register_blueprint(admin_blueprint)

    return app


application = setup_app()

auth_manager = QuartAuth(application)

# -------database-------#
scheduler = AsyncIOScheduler()


async def add_posts_to_db():
    await add_wykop_to_db()
    await add_movies_to_db()
    await add_reddit_to_db()
    await add_youtube_to_db(obtain_key(file_path="CONFIG.json", mode="youtube_key"))


@application.before_serving
async def create_db_tables():
    async with application.app_context():
        db.create_all()
    initialize_platforms()
    await add_posts_to_db()


scheduler.add_job(add_posts_to_db, "interval", hours=2)
scheduler.start()
# -------end database-------#

if __name__ == "__main__":
    asyncio.run(application.run_task(debug=True, host="0.0.0.0", port=5050))
