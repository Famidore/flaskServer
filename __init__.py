from quart import Quart
from flask_sqlalchemy import SQLAlchemy
import asyncio

# db = SQLAlchemy()


def setup_app():
    app = Quart(__name__)

    app.config["SECRET_KEY"] = "gites-malines"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dbs/logindb.sqlite"

    # db.init_app(app)

    from src.auth.auth import auth as auth_blueprint
    from main import main as main_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)

    return app


if __name__ == "__main__":
    asyncio.run(setup_app().run_task(debug=True, host="0.0.0.0", port=5050))
