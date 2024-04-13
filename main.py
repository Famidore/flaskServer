from flask import send_from_directory
from quart import render_template
from quart import Blueprint

from sqlalchemy import text
import os


main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
async def index():
    return await render_template("index.html")


@main.route('/test_2')
def check_db_connection():
    """
    A tu już kurwa jebana nie chce działać, jakie kurwa "The current Flask app is not registered with
    this 'SQLAlchemy' instance. Did you forget to call 'init_app', or did you create multiple 'SQLAlchemy' instances?"
    ja ci kurwa dam forget jebana twoja mać. Ja nic forgot rozumiesz to ty kurwa nie umiesz ogarnąć że to jest registered
    bo jak ci kurwa registeruje to jeszcze raz szmato jebana to zgłaszasz że już masz i żebym urzywał tamtego śmieciu
    jebany. Wszystkie znaki na niebie i ziemi mówią że powinno to gówno dziąłać kurwaaaaaaaaaaaaaaaaa.
    """
    from run import db
    try:

        # Sprawdzenie połączenia z bazą danych
        db.session.execute(text("SELECT 1"))
        return "Pomyślnie połączono z bazą danych!"
    except Exception as e:
        # W razie błędu zwróć komunikat o błędzie
        return f"Błąd podczas łączenia z bazą danych: {e}"


@main.route("/favicon.ico")
async def favicon():
    return await send_from_directory(
        os.path.join(main.root_path, "static"),
        "squid.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@main.route("/time", methods=["GET", "POST"])
async def time():
    return await render_template("time.html")
