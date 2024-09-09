from bs4 import BeautifulSoup

from ai_assistant_parsers_core.common_utils.beautiful_soup import clean_tags, clean_comments, URL_SCHEME_PATTERN

from ..abc import ABCParsingRefiner


class CleanPostParsingRefiner(ABCParsingRefiner):
    def refine(self, html: str) -> str:
        soup = BeautifulSoup(html, "html5lib")

        clean_tags(soup, ["script", "style", "noscript"])
        #clean_tags(soup, ["aside"])
        clean_comments(soup)
        #clean_empty_tags(soup)
        #clean_tags(soup, ["clear", "cls"])
        _clear_javascript_scheme_from_links(soup)

        return str(soup)


def _clear_javascript_scheme_from_links(soup: BeautifulSoup) -> None:
    """
    Example page: https://artesliberales.spbu.ru/ru/faculty
    """
    tag = "a"
    attr = "href"
    for element in soup.find_all(tag, **{attr: True}):
        url = element.get(attr, "").strip()
        if not url:
            continue

        match = URL_SCHEME_PATTERN.match(url)
        if match is None:
            continue

        if match.group(1) == "javascript":
            del element[attr]
