import logging
import os

from dotenv import load_dotenv
from flask import Flask, abort, jsonify, request

from pulse.providers.ecb import ECB
from pulse.providers.eurostat import Eurostat
from pulse.providers.fred import FRED
from pulse.providers.provider import DataProvider

load_dotenv()

app = Flask(__name__)
logger = logging.getLogger(__name__)

PROVIDERS: dict[str, DataProvider] = {
    "FRED": FRED(os.getenv("FRED_API_KEY")),
    "EUROSTAT": Eurostat(),
    "ECB": ECB(),
}


@app.route("/pulse")
async def pulse():
    provider = request.args.get("provider", "fred").upper()
    series_id = request.args.get("series_id")
    frequency = request.args.get("frequency", "d")
    unit = request.args.get("unit", None)
    coicop = request.args.get("coicop", None)
    location = request.args.get("location", None)

    provider = PROVIDERS.get(provider, None)
    if provider is None:
        abort(400, description=f"Invalid provider {provider}")

    observations = await provider.fetch_data(
        series_id, frequency, unit, coicop, location
    )
    metrics_data = await provider.convert_to_time_series(series_id, observations)
    return jsonify(metrics_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
