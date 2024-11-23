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
    filter_key = request.args.get("filter_key", None)
    offset = request.args.get("offset", None)

    provider = PROVIDERS.get(provider, None)
    if provider is None:
        abort(400, description=f"Invalid provider {provider}")

    observations = await provider.fetch_data(series_id, frequency, filter_key)
    metrics_data = await provider.convert_to_time_series(series_id, observations)
    if offset is not None:
        for metric in metrics_data:
            y, etc = metric["timestamp"].split("-", 1)
            y = int(y) - int(offset)
            metric["timestamp"] = f"{y}-{etc}"
    return jsonify(metrics_data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
