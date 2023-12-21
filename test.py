from flask import Flask, render_template, send_from_directory, request
from datetime import datetime
import os

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route("/favicon.ico")
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, "static"),
        "squid.ico",
        mimetype="image/vnd.microsoft.icon",
    )


@app.route("/time", methods=["GET", "POST"])
def time():
    return render_template("time.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
