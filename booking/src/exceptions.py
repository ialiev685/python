from datetime import date

from fastapi import HTTPException, status


class DefaultException(Exception):
    detail: str = "An unexpected error occurred."

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class DefaultHTTPException(HTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class IncorrectTokenException(DefaultException):
    detail: str = "Некорректный токен"


class IncorrectTokenHTTPException(DefaultHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Пользователь не авторизирован'


class NoAccessTokenException(DefaultException):
    detail: str = "Отсутствует токен доступа"


class NoAccessTokenHTTPException(DefaultHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Отсутствует токен доступа'


class ObjectNotFoundException(DefaultException):
    detail: str = "Объект не найден"


class ObjectAlreadyExistsException(DefaultException):
    detail: str = "Объект уже существует"


class UserNotFoundException(ObjectNotFoundException):
    detail: str = "Пользователь не найден"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail: str = "Пользователь уже существует"


class UserNotFoundHTTPException(DefaultHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Пользователь не найден'


class UserAlreadyExistsHTTPException(DefaultHTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = 'Пользователь уже существует'


class IncorrectUserOrPasswordException(DefaultException):
    detail: str = "Неверный логин или пароль"


class IncorrectUserOrPasswordHTTPException(DefaultHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Неверный логин или пароль'


def check_date_from_after_date_to(date_from: date, date_to: date) -> None:
    if date_from >= date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Дата начала не может быть больше даты окончания"
        )


class HotelNotFoundHTTPException(DefaultHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Отель не найден'


class RoomNotFoundHTTPException(DefaultHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Номер не найден'
