import quart_flask_patch
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
from sqlalchemy import text

import asyncio


# TO DO
# Move the connection params to more secure place :D

_PASSWORD = "Trendspire2137"
_USER_ID = "ts_admin"
_SERVER_NAME = "domino403.database.windows.net"
_PORT = "1433"
_DB_NAME = "SQLDataBaseTS"
_ODBC_DRIVER = "ODBC+Driver+18+for+SQL+Server"





def setup_app():
    app = Quart(__name__)

    app.config["SECRET_KEY"] = "gites-malines"
    app.config["SQLALCHEMY_DATABASE_URI"] =\
        f"mssql+pyodbc://{_USER_ID}:{_PASSWORD}@{_SERVER_NAME}:{_PORT}/{_DB_NAME}?driver={_ODBC_DRIVER}"
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


@application.route('/test')
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
