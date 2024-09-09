import abc


class ABCParser(abc.ABC):
    @abc.abstractmethod
    def check(self, url: str) -> bool:
        """Checking url to make sure that url fits parser."""

    @abc.abstractmethod
    def parse(self, html: str) -> str:
        """Parse url.

        :param html: Site html
        :return: Cleaned html
        """
