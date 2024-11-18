import os

import requests
from dotenv import load_dotenv
from flask import Flask, Response

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Fetch FRED API key from environment variables
API_KEY = os.getenv("FRED_API_KEY")
API_URL = "https://api.stlouisfed.org/fred/series/observations"
SERIES_ID = "DGS10"


@app.route("/pulse")
def pulse():
    # Define API request parameters
    params = {
        "series_id": SERIES_ID,
        "api_key": API_KEY,
        "file_type": "json",
        "frequency": "d",
        "sort_order": "desc",
        "limit": 1,
    }

    try:
        response = requests.get(API_URL, params=params)
        data = response.json()

        observations = data.get("observations", [])
        if not observations:
            return Response("# No data available\n", mimetype="text/plain")

        latest_observation = observations[0]
        yield_value = float(latest_observation["value"])
        observation_date = latest_observation["date"]

        # Prepare the Prometheus metrics format
        metrics_data = (
            "# HELP us_bond_yield_10year US 10-Year Treasury Yield\n"
            "# TYPE us_bond_yield_10year gauge\n"
            f'us_bond_yield_10year{{date="{observation_date}"}} {yield_value}\n'
        )

        return Response(metrics_data, mimetype="text/plain")

    except Exception as e:
        return Response(f"# Error fetching data: {str(e)}\n", mimetype="text/plain")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
