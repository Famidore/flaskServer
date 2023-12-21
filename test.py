from flask import Flask
from flask import send_from_directory
from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'), 'squid.ico', mimetype='image/vnd.microsoft.icon')
