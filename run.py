import quart_flask_patch
from quart import Quart
from quart_auth import QuartAuth
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from src.utils import obtain_key
import asyncio

_PASSWORD = obtain_key(mode="_PASSWORD")
_USER_ID = obtain_key(mode="_USER_ID")
_SERVER_NAME = obtain_key(mode="_SERVER_NAME")
_PORT = obtain_key(mode="_PORT")
_DB_NAME = obtain_key(mode="_DB_NAME")
_ODBC_DRIVER = obtain_key(mode="_ODBC_DRIVER")


def setup_app():
    app = Quart(__name__)

    app.config["SECRET_KEY"] = "gites-malines"
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mssql+pyodbc://{_USER_ID}:{_PASSWORD}@{_SERVER_NAME}:{_PORT}/{_DB_NAME}?driver={_ODBC_DRIVER}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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
db = SQLAlchemy(application)


@application.route("/test")
def check_db_connection():
    """
    Tu działa kurwa to jebane DB
    """

    try:
        # Sprawdzenie połączenia z bazą danych
        db.session.execute(text("SELECT 1"))
        return "Pomyślnie połączono z bazą danych!"
    except Exception as e:
        # W razie błędu zwróć komunikat o błędzie
        return f"Błąd podczas łączenia z bazą danych: {e}"


if __name__ == "__main__":
    asyncio.run(application.run_task(debug=True, host="0.0.0.0", port=5050))
