from abc import ABC, abstractmethod


class DataProvider(ABC):
    @abstractmethod
    async def fetch_data(
        self,
        series_id: str,
        frequency: str,
        filter_key: str
    ):
        """
        Fetch time series data from the provider for a given series ID and date range.

        :param series_id: Data series ID (e.g., 'GDP')
        :param frequency: Frequency of data series (e.g., 'q', 'a' or 'd')
        :param filter_key: SDMX filter key (e.g., following the template [FREQ].[UNIT].[NA_ITEM].[GEO])
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
