from quart import Quart
from quart_auth import QuartAuth
from src.utils import obtain_key
import asyncio
from werkzeug.local import LocalProxy


def setup_app():
    app = Quart(__name__)
    app.config["SECRET_KEY"] = obtain_key(mode="app_secret")

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

if __name__ == "__main__":
    asyncio.run(application.run_task(debug=True, host="0.0.0.0", port=5050))
