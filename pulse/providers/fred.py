import logging

import requests

from pulse.providers.provider import DataProvider


class FRED(DataProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.stlouisfed.org/fred/series/observations"
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self, series_id: str, frequency: str, *_):
        params = {
            "series_id": series_id,
            "api_key": self.api_key,
            "file_type": "json",
            "frequency": frequency,
            "sort_order": "desc",
        }

        response = requests.get(self.base_url, params=params)
        data = response.json()
        return data

    async def convert_to_time_series(self, series_id: str, data: dict):
        metrics_data = []
        for observation in data.get("observations", []):
            try:
                metrics_data.append(
                    {
                        "timestamp": observation["date"],
                        "value": float(observation["value"]),
                    }
                )
            # pylint: disable=bare-except
            except:
                self.logger.error(
                    "Failed to get observation for series_id: %s, date: %s, value: %s",
                    series_id,
                    observation["date"],
                    observation["value"],
                )
        return metrics_data
