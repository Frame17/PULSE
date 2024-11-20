from abc import ABC, abstractmethod


class DataProvider(ABC):
    @abstractmethod
    async def fetch_data(
        self,
        series_id: str,
        frequency: str,
        unit: str,
        coicop: str,
        location: str
    ):
        """
        Fetch time series data from the provider for a given series ID and date range.

        :param series_id: Data series ID (e.g., 'GDP')
        :param frequency: Frequency of data series (e.g., 'q', 'a' or 'd')
        :param unit: unit of measure
        :param coicop: Classification of Individual Consumption by Purpose
        :param location: country (e.g., 'DE')
        :return: JSON data from the provider
        """

    @abstractmethod
    async def convert_to_time_series(self, series_id: str, data: dict):
        """
        Convert the fetched data into a common format: list of dictionaries with "timestamp" and "value".

        :param data: JSON data returned from the provider
        :param series_id: Data series ID (e.g., 'GDP')
        :return: List of dictionaries with "timestamp" and "value"
        """
