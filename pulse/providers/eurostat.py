import logging

import requests

from pulse.providers.provider import DataProvider

Q_MONTH_MAPPING: dict[str, str] = {"Q1": "01", "Q2": "04", "Q3": "07", "Q4": "10"}

class Eurostat(DataProvider):
    def __init__(self):
        # pylint: disable=line-too-long
        self.base_url = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/data/{dataset_id}/{filter_key}?format=JSON"
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self, series_id: str, frequency: str, filter_key: str):
        params = {"dataset_id": series_id.upper(), "filter_key": filter_key.upper()}
        response = requests.get(self.base_url.format(**params))
        return response.json()

    async def convert_to_time_series(self, series_id: str, data: dict):
        time_labels = {
            str(value): key
            for key, value in data["dimension"]["time"]["category"]["index"].items()
        }
        values = data["value"]

        metrics_data = []
        for key, value in values.items():
            try:
                timestamp = time_labels[key]
                if "Q" in timestamp:
                    y, q = timestamp.split("-")
                    timestamp = f"{y}-{Q_MONTH_MAPPING[q]}"
                metrics_data.append({"timestamp": timestamp, "value": float(value)})
            # pylint: disable=bare-except
            except:
                self.logger.error(
                    "Failed to get EUROSTAT observation for series_id: %s, date: %s, value: %s",
                    series_id,
                    timestamp,
                    value,
                )
        return metrics_data
