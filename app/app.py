from flask import Flask, jsonify, render_template

from clearmycal import get_historical, get_forecast
from cmc import main
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", temp=42)


@app.route("/api/<location>")
def api(location):
    return jsonify(f"Hello, {location}")

@app.route("/api/wx/<location>")
def cal(location):
    alert = main(location)

    return jsonify(f"ALERT:  {alert[0]}  for location {location}")
