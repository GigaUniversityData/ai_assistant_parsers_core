from bs4 import BeautifulSoup

from ai_assistant_parsers_core.refiners import ABCParsingRefiner
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_all_by_select
from ai_assistant_parsers_core.parsers.utils.restructure_blocks import rename_all_by_select




class RestructureTablesParsingRefiner(ABCParsingRefiner):
    def refine(self, soup: BeautifulSoup) -> str:
        clean_all_by_select(soup, ".table__col-title")  # Имеет `display: none;`
        rename_all_by_select(soup, "div.table", "table")
        rename_all_by_select(soup, "div.table__row", "tr")
        rename_all_by_select(soup, "div.table__cell", "td")
        rename_all_by_select(
            soup,
            ".table__row_header > td.table__cell",
            "th",
        )

        return str(soup)
