import datetime as dt
import openai

from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os

from Types.InvalidUsage import InvalidUsage
from get_weather import resolve_weather

load_dotenv()

API_TOKEN = os.environ.get("API_TOKEN")
RSA_KEY = os.environ.get("RSA_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_KEY")

app = Flask(__name__)
client = openai.OpenAI(api_key=OPENAI_API_KEY)


def get_advice(weather):
    prompt = (f"Based on the following weather conditions, "
              f"suggest what to wear: {weather} Provide a short, practical recommendation.")
    try:
        response = client.chat.completions.create(
            model="omni-moderation-latest",
            messages=[
                {"role": "user",
                 "content": prompt
                 }]
        )
    except Exception as e:
        return "GPT response went wrong"

    return response["choices"][0]["message"]["content"]


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
        raise InvalidUsage(f"wrong API token {token} needed {API_TOKEN}", status_code=403)

    weather = resolve_weather(RSA_KEY, location=location, date=date)
    advice = get_advice(weather)

    end_dt = dt.datetime.now()

    result = {
        "requester_name": requester_name,
        "timestamp": end_dt.strftime("%m/%d/%Y, %H:%M:%S"),
        "location": location,
        "date": date,
        "weather": weather,
        "cloth_advice": advice
    }

    return result
