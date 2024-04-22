import quart_flask_patch
from quart import Quart
from quart_auth import QuartAuth
from src.pages.posts_db.models import db
from src.pages.posts_db.adding_posts import add_movies_to_db
import asyncio

from src.utils import obtain_key


def setup_app():
    app = Quart(__name__)
    app.config["SECRET_KEY"] = "gites-malines"
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:gites-malines@localhost/database"
    db.init_app(app)
    QuartAuth(app)

    from src.auth.auth import auth as auth_blueprint
    from main import main as main_blueprint
    from src.trends import trending as trending_blueprint
    from src.premium_pages.premium_sites import premium as premium_blueprint
    from src.user_profile.profile import user_profile as profile_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(trending_blueprint)
    app.register_blueprint(premium_blueprint)
    app.register_blueprint(profile_blueprint)

    return app


application = setup_app()


async def before_serving():
    from src.pages.posts_db.adding_posts import add_wykop_to_db, add_movies_to_db, add_youtube_to_db, add_reddit_to_db
    await add_wykop_to_db()
    await add_movies_to_db()
    await add_reddit_to_db()
    await add_youtube_to_db(obtain_key(file_path="CONFIG.json", mode="youtube_key"))


@application.before_serving
async def call_adding_to_db():
    async with application.app_context():
        db.create_all()
    await before_serving()

if __name__ == "__main__":
    asyncio.run(application.run_task(debug=True, host="0.0.0.0", port=5050))
