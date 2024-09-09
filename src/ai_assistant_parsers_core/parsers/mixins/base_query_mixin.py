import abc
from bs4 import BeautifulSoup


class BaseQueryMixin(abc.ABC):
    def parse(self, html: str) -> str:
        source_html = BeautifulSoup(html, "html5lib")
        cleaned_html = BeautifulSoup("<html><body></body></html>", "html.parser")

        self._prepare_result(source_html, cleaned_html)

        self._clean_parsed_html(cleaned_html)
        self._restructure_parsed_html(cleaned_html)

        return str(cleaned_html)

    @abc.abstractmethod
    def _prepare_result(self, soup: BeautifulSoup, result: BeautifulSoup) -> None:
        pass

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        pass

    def _restructure_parsed_html(self, soup: BeautifulSoup) -> None:
        pass
