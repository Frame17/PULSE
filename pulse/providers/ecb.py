import logging

import requests

from pulse.providers.provider import DataProvider


class ECB(DataProvider):
    def __init__(self):
        # pylint: disable=line-too-long
        self.base_url = (
            "https://data-api.ecb.europa.eu/service/data/{flow_ref}/{filter_key}"
        )
        self.logger = logging.getLogger(__name__)

    async def fetch_data(self, series_id: str, *_):
        flow_ref, filter_key = series_id.upper().split(".", 1)
        params = {"flow_ref": flow_ref, "filter_key": filter_key}
        url = self.base_url.format(**params)
        response = requests.get(url, headers={"Accept": "application/json"}, )
        return response.json()

    async def convert_to_time_series(self, series_id: str, data: dict):
        time_labels = data["structure"]["dimensions"]["observation"][0]["values"]
        values = data["dataSets"][0]["series"][":".join(["0"] * series_id.count("."))][
            "observations"
        ]

        metrics_data = []
        for key, value in values.items():
            try:
                timestamp = time_labels[int(key)]["name"]
                metrics_data.append({"timestamp": timestamp, "value": float(value[0])})
            # pylint: disable=bare-except
            except:
                self.logger.error(
                    "Failed to get ECB observation for series_id: %s, date: %s, value: %s",
                    series_id,
                    timestamp,
                    value[0],
                )

        return metrics_data
