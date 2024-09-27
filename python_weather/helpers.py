from datetime import datetime

format = "%Y-%m-%d"


def is_valid_date(start_date: str, end_date: str):

    start_dt, end_dt = convert_period_dates_to_datetime_format(start_date, end_date)

    is_period = bool(start_dt and end_dt)

    try:
        if datetime.now().date() > start_dt.date():
            raise ValueError("Стартовая дата не должна быть ранше текущей")

        if is_period and (end_dt - start_dt).days > 30:
            raise ValueError("разница между датами не должна превышать более 30 дней")

        if is_period and start_dt > end_dt:
            raise ValueError("стартовая дата должа быть раньше чем конечная дата")

        return True
    except ValueError as error:
        print("дата не валидна:", error)
        return False


def convert_period_dates_to_datetime_format(
    start_date: str, end_date: str
) -> tuple[datetime, datetime | None]:

    try:
        if start_date and end_date:
            start_dt = datetime.strptime(start_date, format)
            end_dt = datetime.strptime(end_date, format)

            return start_dt, end_dt
        else:
            start_dt = datetime.strptime(start_date, format)

            return start_dt, None
    except ValueError as error:
        print("Ошибка в конрвертации периода дат: ", error)
    except TypeError as error:
        print("error", error)
