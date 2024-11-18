import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, Response, request

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("FRED_API_KEY")
API_URL = "https://api.stlouisfed.org/fred/series/observations"


def fetch_fred_data(series_id: str, frequency: str):
    params = {
        "series_id": series_id,
        "api_key": API_KEY,
        "file_type": "json",
        "frequency": frequency,
        "sort_order": "desc",
    }

    response = requests.get(API_URL, params=params)
    data = response.json()
    return data.get("observations", [])


@app.route("/pulse")
def metrics():
    series_id = request.args.get("series_id")
    series_name = request.args.get("series_name")
    frequency = request.args.get("frequency", "d")

    observations = fetch_fred_data(series_id, frequency)
    if not observations:
        return Response("# No data available\n", mimetype="text/plain")

    try:
        latest_observation = observations[0]
        yield_value = float(latest_observation["value"])
    # pylint: disable=bare-except
    except:
        latest_observation = observations[1]
        yield_value = float(latest_observation["value"])

    observation_date = latest_observation["date"]
    metrics_data = (
        f"# TYPE {series_name} gauge\n"
        f'{series_name}{{date="{observation_date}"}} {yield_value}\n'
    )

    return Response(metrics_data, mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
