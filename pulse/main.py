import logging
import os

import requests
from dotenv import load_dotenv
from flask import Flask, Response, jsonify, request

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

API_KEY = os.getenv("FRED_API_KEY")
API_URL = "https://api.stlouisfed.org/fred/series/observations"


async def fetch_fred_data(series_id: str, frequency: str):
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
async def pulse():
    series_id = request.args.get("series_id")
    frequency = request.args.get("frequency", "d")

    observations = await fetch_fred_data(series_id, frequency)
    if not observations:
        return Response("# No data available\n", mimetype="text/plain")

    metrics_data = []
    for observation in observations:
        try:
            metrics_data.append(
                {
                    "timestamp": observation["date"],
                    "value": float(observation["value"]),
                }
            )
        # pylint: disable=bare-except
        except:
            logger.error(
                "Failed to get observation for series_id: %s, date: %s, value: %s",
                series_id,
                observation["date"],
                observation["value"]
            )
    return jsonify(metrics_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
