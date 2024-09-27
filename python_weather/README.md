python -m venv [название_окружения]

[название_окружения]\Scripts\activate.bat - для Windows;
source [название_окружения]/bin/activate - для Linux и MacOS.

Пример:

python weather.py 2024-01-01 -e 2024-01-10 -r -s
запрос на апи с сохарнением

pip freeze > requirements.txt - записать зависимости
pip install -r requirements.txt - установить зависимости
