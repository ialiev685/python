import peewee
from peewee import DatabaseProxy
from helpers import convert_period_dates_to_datetime_format
from playhouse.db_url import connect

database_proxy = DatabaseProxy()

# database = peewee.SqliteDatabase("weather_data/weather.db")


class BaseTable(peewee.Model):
    class Meta:
        database = database_proxy


class City(BaseTable):
    name = peewee.CharField()


class Weather(BaseTable):
    weather = peewee.CharField()
    temperature = peewee.CharField()
    date = peewee.DateField()
    city = peewee.ForeignKeyField(City, backref="weathers")


# database.create_tables([City, Weather])


class DatabaseUpdater:
    def __init__(self, url) -> None:
        database = connect(f"sqlite:///{url}")
        database_proxy.initialize(database)

        database.create_tables([City, Weather])

    def get_city(self, name: str):
        try:
            found_city = City.get(City.name == name)
            return found_city
        except peewee.DoesNotExist:
            return None

    def add_weather_data(self, name_city: str, weather_data: list[dict]):
        try:

            found_city = self.get_city(name=name_city.lower())

            city = found_city if found_city else City.create(name=name_city.lower())

            formated_weather_data = map(
                lambda value: {**value, "city": city},
                weather_data,
            )

            search_dates_array = map(lambda value: value["date"], weather_data)

            exists_dates = Weather.select().where(
                (Weather.date.in_(list(search_dates_array)) & (Weather.city == city))
            )

            exists_dates_set = {row.date.strftime("%Y-%m-%d") for row in exists_dates}
            print(exists_dates_set)

            filtered_formated_weather_data = filter(
                lambda value: value["date"] not in exists_dates_set,
                formated_weather_data,
            )

            query: peewee.ModelInsert = Weather.insert_many(
                filtered_formated_weather_data
            )

            query.execute()

        except:
            print("Возникла ошибка при сохранении данный в БД:")

    def get_weather_data(self, city: str, start_date: str, end_date: str | None):
        try:
            start_dt, end_dt = convert_period_dates_to_datetime_format(
                start_date, end_date
            )

            found_city = self.get_city(name=city)

            query = None

            if start_dt and end_dt:
                query: peewee.ModelSelect = Weather.select().where(
                    (Weather.date >= start_dt)
                    & (Weather.date <= end_dt)
                    & (Weather.city == found_city)
                )

            else:
                query: peewee.ModelSelect = Weather.select().where(
                    (Weather.date == start_dt) & (Weather.city == found_city)
                )

            return [
                {
                    "weather": row.weather,
                    "temperature": row.temperature,
                    "date": row.date.strftime("%Y-%m-%d"),
                    "city": row.city.name,
                }
                for row in query
            ]

        except peewee.DoesNotExist:
            return None
