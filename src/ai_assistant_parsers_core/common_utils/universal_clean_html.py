from bs4 import BeautifulSoup, Tag

from ai_assistant_parsers_core.common_utils.beautiful_soup import clean_tags, clean_comments


def universal_clean_html(html_src: str) -> str:
    soup = BeautifulSoup(html_src, "html5lib")

    soup = soup.find("body") or soup
    soup = soup.find("main") or soup

    clean_tags(soup, ["script", "style", "noscript", "nav", "head", "footer", "header"])
    #_clean_specific_css(soup)
    clean_comments(soup)
    #clean_empty_tags(soup)

    # Очитка атрибутов
    _clean_attributes(soup)

    soup.name = "html"

    return str(soup)


def _clean_specific_css(soup: BeautifulSoup) -> None:
    """Удаляет теги по селектору."""
    for tag in soup.select('div[id*="google-cache-hdr"], div[id*="wm-ipp"], div[class*="bread"], ul[class*="bread"], div[class*="menu"], li[class*="menu"], section[class*="anchors"]'):
        tag.decompose()


def _clean_attributes(soup: BeautifulSoup) -> None:
    """Remove unwanted attributes and convert relative links to absolute."""
    tag: Tag

    for tag in soup.find_all(True):  # True finds all tags
        attrs_to_remove = [attr for attr in tag.attrs if attr not in ["text", "src", "href"]]
        for attr in attrs_to_remove:
            del tag[attr]
