from flask import Flask
from flask import send_from_directory
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'squid.ico', mimetype='image/vnd.microsoft.icon')
