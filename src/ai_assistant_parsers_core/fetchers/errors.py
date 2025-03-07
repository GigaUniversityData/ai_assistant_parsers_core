

class FetcherError(Exception):
    """Базовое исключение для ошибок фетчера."""


class InvalidAuthorizationError(FetcherError):
    """Ошибка, когда не заданы параметры авторизации."""


class FetcherNotOpenError(FetcherError):
    """Ошибка, когда фетчер не открыт (сессия не инициализирована)."""


class ServerConnectionError(FetcherError):
    def __str__(self) -> str:
        return "Cannot connect to FetchingAPI server"


class ServerResponseError(FetcherError):
    pass
