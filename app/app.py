from flask import Flask, jsonify, render_template, request
from .cmc import main

app = Flask(__name__)


@app.route("/")
def index():
    try: 
        location = 'Oxford'
        temp = main(location)
        return render_template("index.html", temp=temp, location=location)
    except:
        return render_template("index.html", temp='no data',location=location)


@app.route("/api/<location>")
def api(location):
    return jsonify(f"Hello, {location}")

@app.route("/api/wx/<location>")
def cal(location):
    alert = main(location)

    return jsonify(f"ALERT:  {alert[0]}  for location {location}")
