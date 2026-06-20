from mcp.server.fastmcp import FastMCP

from clients.nws_client import NWSClient
from services.weather_service import WeatherService
from formatters.alert_formatter import AlertFormatter


mcp = FastMCP("weather")

service = WeatherService(
    nws_client=NWSClient()
)


@mcp.tool()
async def get_alerts(state: str) -> str:

    data = await service.get_alerts(state)

    if not data:
        return "No alerts found."

    alerts = [
        AlertFormatter.format(feature)
        for feature in data["features"]
    ]

    return "\n---\n".join(alerts)


@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:

    data = await service.get_forecast(latitude, longitude)

    if not data:
        return "Unable to fetch forecast data for this location."

    periods = data["properties"]["periods"]
    forecasts = []
    for period in periods[:5]:
        forecasts.append(
            (
                f"{period['name']}:\n"
                f"Temperature: {period['temperature']}°{period['temperatureUnit']}\n"
                f"Wind: {period['windSpeed']} {period['windDirection']}\n"
                f"Forecast: {period['detailedForecast']}"
            )
        )

    return "\n---\n".join(forecasts)