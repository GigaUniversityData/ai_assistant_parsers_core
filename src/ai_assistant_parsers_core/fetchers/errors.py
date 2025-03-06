

class FetcherError(Exception):
    """Базовое исключение для ошибок фетчера."""

class InvalidAuthorizationError(FetcherError):
    """Ошибка, когда не заданы параметры авторизации."""

class FetcherNotOpenError(FetcherError):
    """Ошибка, когда фетчер не открыт (сессия не инициализирована)."""
