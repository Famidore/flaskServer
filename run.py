from quart import Quart
from quart_auth import (
    AuthUser,
    current_user,
    login_required,
    login_user,
    logout_user,
    QuartAuth,
)
from flask_sqlalchemy import SQLAlchemy
import asyncio

db = SQLAlchemy()


def setup_app():
    app = Quart(__name__)

    app.config["SECRET_KEY"] = "gites-malines"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbs/db.sqlite"

    QuartAuth(app)

    # with app.app_context():
    #     db.init_app(app)

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


if __name__ == "__main__":
    asyncio.run(setup_app().run_task(debug=True, host="0.0.0.0", port=5050))
