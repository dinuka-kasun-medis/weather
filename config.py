from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    nws_api_base: str = "https://api.weather.gov"
    timeout_seconds: float = 30.0
    user_agent: str = "weather-app/1.0"


settings = Settings()