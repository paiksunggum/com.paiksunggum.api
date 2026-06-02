from .openweather_reader import OpenWeatherReader
from .schemas import WeatherResponse


class WeatherService:
    def __init__(self) -> None:
        self.reader = OpenWeatherReader()

    async def get_current(
        self,
        *,
        city: str | None = None,
        lat: float | None = None,
        lon: float | None = None,
    ) -> WeatherResponse:
        if not self.reader.api_key:
            return WeatherResponse(
                city=city or "Seoul",
                temp_c=0,
                description="날씨 API 미설정",
                icon="01d",
            )

        data = await self.reader.fetch_current(city=city, lat=lat, lon=lon)
        weather = data["weather"][0]
        return WeatherResponse(
            city=data["name"],
            temp_c=round(float(data["main"]["temp"])),
            description=weather["description"],
            icon=weather["icon"],
        )
