from datetime import date

from fastapi import HTTPException, status


class DefaultException(Exception):
    detail: str = "An unexpected error occurred."

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(DefaultException):
    detail: str = "Объект не найден"


class ObjectAlreadyException(DefaultException):
    detail: str = "Объект уже существует"


def check_date_from_after_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата начала не может быть больше даты окончания"
        )


class DefaultHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(DefaultException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Отель не найден'


class RoomNotFoundHTTPException(DefaultException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Номер не найден'
