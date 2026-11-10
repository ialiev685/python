class DefaultException(Exception):
    detail: str = "An unexpected error occurred."

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class IncorrectDateRangeException(DefaultException):
    detail: str = "Дата начала не может быть больше даты окончания"


class NotFoundException(DefaultException):
    detail: str = "Объект не найден"


class ConflictException(DefaultException):
    detail: str = "Объект уже существует"
