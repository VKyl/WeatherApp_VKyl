import datetime as dt

from flask import Flask, jsonify, request
import os

from Types.InvalidUsage import InvalidUsage
from get_weather import resolve_weather

API_TOKEN = os.environ.get("API_TOKEN")
RSA_KEY = os.environ.get("RSA_KEY")

app = Flask(__name__)


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/")
def home_page():
    return "<h2>Weather Forecast App</h2>"


@app.route("/content/api/v1/integration/generate", methods=["GET"])
def weather_endpoint():
    json_data = request.get_json()

    token = json_data.get("token")
    requester_name = json_data.get("requester_name")
    location = json_data.get("location")
    date = json_data.get("date")

    if token is None:
        raise InvalidUsage("token is required", status_code=400)

    if token != API_TOKEN:
        raise InvalidUsage("wrong API token", status_code=403)

    weather = resolve_weather(RSA_KEY, location=location, date=date)

    end_dt = dt.datetime.now()

    result = {
        "requester_name": requester_name,
        "timestamp": end_dt.strftime("%m/%d/%Y, %H:%M:%S"),
        "location": location,
        "date": date,
        "weather": weather
    }

    return result
