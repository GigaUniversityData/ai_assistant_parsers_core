"""Абстракции для фетчеров."""

import abc


class ABCFetcher(abc.ABC):
    """Абстрактный фетчер."""

    @abc.abstractmethod
    async def open(self) -> None:
        """Открывает фетчер."""

    @abc.abstractmethod
    async def fetch(self, url: str) -> str:
        """Извлекает HTML из URL-адреса.

        Args:
            url (str): URL-адрес.

        Returns:
            str: HTML-код.
        """

    @abc.abstractmethod
    async def close(self) -> None:
        """Закрывает фетчер."""

    @abc.abstractmethod
    def is_open(self) -> bool:
        """Проверяет открыт ли фетчер.

        Returns:
            bool: Результат.
        """
