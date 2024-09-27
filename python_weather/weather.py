# -*- coding: utf-8 -*-

# В очередной спешке, проверив приложение с прогнозом погоды, вы выбежали
# навстречу ревью вашего кода, которое ожидало вас в офисе.
# И тут же день стал хуже - вместо обещанной облачности вас встретил ливень.

# Вы промокли, настроение было испорчено, и на ревью вы уже пришли не в духе.
# В итоге такого сокрушительного дня вы решили написать свою программу для прогноза погоды
# из источника, которому вы доверяете.

# Для этого вам нужно:

# Создать модуль-движок с классом WeatherMaker, необходимым для получения и формирования предсказаний.
# В нём должен быть метод, получающий прогноз с выбранного вами сайта (парсинг + re) за некоторый диапазон дат,
# а затем, получив данные, сформировать их в словарь {погода: Облачная, температура: 10, дата:datetime...}

# Добавить класс ImageMaker.
# Снабдить его методом рисования открытки
# (использовать OpenCV, в качестве заготовки брать lesson_016/python_snippets/external_data/probe.jpg):
#   С текстом, состоящим из полученных данных (пригодится cv2.putText)
#   С изображением, соответствующим типу погоды
# (хранятся в lesson_016/python_snippets/external_data/weather_img ,но можно нарисовать/добавить свои)
#   В качестве фона добавить градиент цвета, отражающего тип погоды
# Солнечно - от желтого к белому
# Дождь - от синего к белому
# Снег - от голубого к белому
# Облачно - от серого к белому

# Добавить класс DatabaseUpdater с методами:
#   Получающим данные из базы данных за указанный диапазон дат.
#   Сохраняющим прогнозы в базу данных (использовать peewee)

# Сделать программу с консольным интерфейсом, постаравшись все выполняемые действия вынести в отдельные функции.
# Среди действий, доступных пользователю, должны быть:
#   Добавление прогнозов за диапазон дат в базу данных
#   Получение прогнозов за диапазон дат из базы
#   Создание открыток из полученных прогнозов
#   Выведение полученных прогнозов на консоль
# При старте консольная утилита должна загружать прогнозы за прошедшую неделю.

# Рекомендации:
# Можно создать отдельный модуль для инициализирования базы данных.
# Как далее использовать эту базу данных в движке:
# Передавать DatabaseUpdater url-путь
# https://peewee.readthedocs.io/en/latest/peewee/playhouse.html#db-url
# Приконнектится по полученному url-пути к базе данных
# Инициализировать её через DatabaseProxy()
# https://peewee.readthedocs.io/en/latest/peewee/database.html#dynamically-defining-a-database


from weather_maker import WeatherMaker
from image_maker import ImageMaker
from helpers import is_valid_date
from playhouse.db_url import connect
from pprint import pprint
from database_updater import DatabaseUpdater

import argparse

db_path = "weather_data/weather.db"


parser = argparse.ArgumentParser(description="weather commands")
parser.add_argument("city", help="название города")
parser.add_argument("start_dt", help="начало даты, формат=YYYY-mm-dd")
parser.add_argument("-e", "--end", help="конец даты, формат=YYYY-mm-dd")
parser.add_argument("-d", "--draw", action="store_true", help="рисовать карточки")
parser.add_argument(
    "-r", "--request", action="store_true", help="запросить данные с сервера"
)
parser.add_argument(
    "-db", "--database", action="store_true", help="запросить данные с баззы данных"
)
parser.add_argument(
    "-s", "--save", action="store_true", help="сохранить данные с базу данных"
)

args = parser.parse_args()


city = args.city
start_date = args.start_dt
end_date = args.end
is_draw_cards = args.draw
is_request = args.request
is_from_db = args.database
is_save_to_database = args.save


if is_valid_date(start_date, end_date) is True:
    try:
        database_updater = DatabaseUpdater(url=db_path)

        result_weather = None

        if is_request and is_from_db:
            raise ValueError("Нельзя одновременно запрашивать из базы и из сервера")

        if is_from_db and is_save_to_database:
            raise ValueError(
                "Нельзя одновременно запрашивать из базы и сохранять в базу"
            )

        if is_from_db and is_request is False:
            result_weather = database_updater.get_weather_data(
                city=city, start_date=start_date, end_date=end_date
            )

        if is_request and is_from_db is False:
            weatherMaker = WeatherMaker(
                city=city, start_date=start_date, end_date=end_date
            )
            result_weather = weatherMaker.weather_by_day

            if is_save_to_database:
                database_updater.add_weather_data(city, weatherMaker.weather_by_day)

        print("=================")
        print("результат погоды:")
        print("=================")
        pprint(result_weather)

        if is_draw_cards:
            imageMaker = ImageMaker(options=result_weather)

            imageMaker.draw_cards()
    except ValueError as error:
        print("ошибка:", error)
