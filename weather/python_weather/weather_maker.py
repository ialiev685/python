import requests
import re


from helpers import convert_period_dates_to_datetime_format

API_KEY = "e59be2fdbcb84c81896202449241007"

lat_city = 55.7823547
lon_city = 49.1242266


def make_url(city: str, start_date: str, end_date: str):

    # по широте и долготе
    # WEATHER_API_URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={lat_city},{lon_city}&days=4&hour_fields=temp_c&lang=ru&aqi=no&tides=no"
    # по названию
    start_dt, end_dt = convert_period_dates_to_datetime_format(start_date, end_date)

    days = (end_dt - start_dt).days if end_dt and start_dt else 1

    WEATHER_API_URL = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={city}&days={days}&hour_fields=temp_c&lang=ru&aqi=no&tides=no"
    # WEATHER_API_URL = f"http://api.weatherapi.com/v1/history.json?key={API_KEY}&q={city}&dt={start_date}&end_dt={end_date}&hour_fields=temp_c&lang=ru&aqi=no&tides=no"

    return WEATHER_API_URL


class WeatherMaker:
    def __init__(self, city: str, start_date: str, end_date: str) -> None:

        self.start_date = start_date
        self.end_date = end_date

        self.weather_by_day = None
        self.get_parsed_weather_data(city=city)

    def get_raw_weather_data(self, city: str):
        result = requests.get(make_url(city, self.start_date, self.end_date))
        return result.json()

    def parsing_weather_text(self, value: str):

        snow_pattern = r"снег"
        rain_pattern = r"дожд"
        cloud_pattern = r"облач"
        sun_pattern = r"солнеч"

        if re.search(sun_pattern, value, re.IGNORECASE):
            return "sunny"
        if re.search(snow_pattern, value, re.IGNORECASE):
            return "snow"
        if re.search(rain_pattern, value, re.IGNORECASE):
            return "rain"
        if re.search(cloud_pattern, value, re.IGNORECASE):
            return "cloudy"

        return None

    def get_parsed_weather_data(self, city: str):
        data = self.get_raw_weather_data(city=city)
        if isinstance(data, dict):
            if "location" in data and "forecast" in data:

                location, forecast = data["location"], data["forecast"]

                weather_by_day = []

                for day in forecast["forecastday"]:
                    weather = day["day"]["condition"]["text"]
                    city = location["name"]
                    date = day["date"]
                    temperature = day["day"]["avgtemp_c"]

                    weather_by_day.append(
                        {
                            "weather": self.parsing_weather_text(weather),
                            "temperature": f"t {str(round(temperature))}",
                            "date": date,
                            "city": city,
                        }
                    )
                self.weather_by_day = weather_by_day

                return weather_by_day
