from airflow.models import BaseOperator
import requests
from datetime import datetime


class WeatherApiOperator(BaseOperator):
    def __init__(
        self,
        lattitude: float,
        longitude: float,
        hours_ahead: int = 1,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.latitude = lattitude
        self.longitude = longitude
        self.hours_ahead = hours_ahead

    def _get_weather_forecast(self):
        """Fetch weather forecast data from Open-Meteo API."""
        url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={self.latitude}"
            f"&longitude={self.longitude}"
            "&hourly=temperature_2m,precipitation_probability,wind_speed_10m,apparent_temperature"
            "&forecast_days=1"
            "&timezone=Europe%2FLondon"
        )

        res = requests.get(url)
        res.raise_for_status()
        data = res.json()

        time_list = data["hourly"]["time"]
        temp = data["hourly"]["temperature_2m"]
        rain_prob = data["hourly"].get("precipitation_probability", [])
        wind = data["hourly"]["wind_speed_10m"]
        feels = data["hourly"]["apparent_temperature"]

        # get current time in Europe/London (naive comparison with API times)
        now = datetime.now()

        # find index of the first forecast >= current hour
        start_idx = next(
            (i for i, t in enumerate(time_list) if datetime.fromisoformat(t) >= now),
            0
        )

        slice_end = min(start_idx + self.hours_ahead, len(time_list))

        forecast = []
        for i in range(start_idx, slice_end):
            forecast.append({
                "time": time_list[i],
                "temperature_c": temp[i],
                "rain_chance_pct": rain_prob[i] if i < len(rain_prob) else None,
                "wind_speed_kmh": wind[i],
                "feels_like_c": feels[i]
            })

        return forecast

    def execute(self, context):
        forecast = self._get_weather_forecast()
        return forecast