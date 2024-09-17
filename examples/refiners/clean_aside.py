from bs4 import BeautifulSoup

from ai_assistant_parsers_core.refiners import ABCParsingRefiner
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_all_by_select


class CleanASideParsingRefiner(ABCParsingRefiner):
    def refine(self, html: str) -> str:
        soup = BeautifulSoup(html, "html5lib")
        clean_all_by_select(soup, "aside")
        return str(soup)
