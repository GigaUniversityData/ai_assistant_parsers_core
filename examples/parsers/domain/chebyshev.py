from bs4 import BeautifulSoup

from ai_assistant_parsers_core.parsers import ABCParser, DomainMixin, BaseQueryMixin
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_all_by_select
from ai_assistant_parsers_core.parsers.utils.restructure_blocks import rename_all_by_select


class ChebyshevDomainParser(
    BaseQueryMixin,
    DomainMixin,
    ABCParser,
):
    def __init__(self) -> None:
        super().__init__(
            supported_subdomains=["chebyshev.spbu.ru"],
            unsupported_paths=["/", "/people/*"],
        )

    def _prepare_result(self, source_html: BeautifulSoup, cleaned_html: BeautifulSoup) -> None:
        tags = source_html.select(":has(> h2)")

        for tag in tags:
            cleaned_html.html.body.append(tag)

    def _restructure_parsed_html(self, soup: BeautifulSoup) -> None:
        # Обработка таблиц
        clean_all_by_select(soup, ".courses-table__col-title")  # Имеет `display: none;`
        rename_all_by_select(soup, "div.courses-table", "table")
        rename_all_by_select(soup, "div.courses-table__row", "tr")
        rename_all_by_select(soup, "div.courses-table__cell", "td")
        rename_all_by_select(
            soup,
            ".courses-table__row_header > td.courses-table__cell",
            "th",
        )

        # Обработка таблиц у URL-адресе https://chebyshev.spbu.ru/conferences/
        clean_all_by_select(soup, ".table__col-title")  # Имеет `display: none;`
        rename_all_by_select(soup, "div.table", "table")
        rename_all_by_select(soup, "div.table__row", "tr")
        rename_all_by_select(soup, "div.table__cell", "td")
        rename_all_by_select(
            soup,
            ".table__row_header > td.table__cell",
            "th",
        )
