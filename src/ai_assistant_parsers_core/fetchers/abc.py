"""Абстракции для фетчеров."""

import abc

from ai_assistant_parsers_core.magic_url import MagicURL


class ABCFetcher(abc.ABC):
    """Абстрактный фетчер."""

    @abc.abstractmethod
    async def open(self) -> None:
        """Открывает фетчер."""

    @abc.abstractmethod
    async def fetch(self, magic_url: MagicURL) -> str:
        """Извлекает HTML из URL-адреса.

        Args:
            magic_url (MagicURL): URL-адрес.

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
