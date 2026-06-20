import logging

from clients.nws_client import NWSClient
from config import settings

logger = logging.getLogger(__name__)


class WeatherService:

    def __init__(self, nws_client: NWSClient):
        self._nws_client = nws_client

    async def get_alerts(
        self,
        state: str,
    ):

        state = state.upper()

        if len(state) != 2:
            raise ValueError(
                "State must be a two-letter code."
            )

        url = (
            f"{settings.nws_api_base}"
            f"/alerts/active/area/{state}"
        )

        return await self._nws_client.get_json(url)

    async def get_forecast(
        self,
        latitude: float,
        longitude: float,
    ):

        if not (-90 <= latitude <= 90):
            raise ValueError("Invalid latitude")

        if not (-180 <= longitude <= 180):
            raise ValueError("Invalid longitude")

        points_url = (
            f"{settings.nws_api_base}"
            f"/points/{latitude},{longitude}"
        )

        points = await self._nws_client.get_json(
            points_url
        )

        if not points:
            return None

        forecast_url = points["properties"]["forecast"]

        return await self._nws_client.get_json(
            forecast_url
        )