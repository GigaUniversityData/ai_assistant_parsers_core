import re

from bs4 import BeautifulSoup, Tag

from ..abc import ABCParsingRefiner


STYLE_TAGS_REGEX = re.compile(r"""
^(?:
    h[1-6]         # Заголовки h1-h6
    | strong       # Жирный текст (строгий)
    | b            # Жирный текст
    | i            # Курсив
    | em           # Выделение (обычно курсив)
    | mark         # Выделение маркером
    | small        # Мелкий текст
    | del          # Удаленный текст
    | ins          # Вставленный текст
    | sub          # Нижний индекс
    | sup          # Верхний индекс
    | u            # Невыраженная аннотация (Волнистое подчеркивание).
)$
""", flags=re.VERBOSE)


class RestructurePostParsingRefiner(ABCParsingRefiner):
    """
    Производит изменение структуры "очищенного HTML-кода" для улучшения его читаемости.
     
    NOTE:
        Рекомендуется применять после парсинга.
    """

    def refine(self, html: str) -> str:
        """Реализует метод ``refine`` базового абстрактного класса."""

        soup = BeautifulSoup(html, "html5lib")

        _clean_empty_style_tags(soup)
        _clean_empty_list_items(soup)

        return str(soup)


def _clean_empty_style_tags(soup: BeautifulSoup) -> None:
    """Очищает пустые HTML-теги стиля (``h1``, ``b``, ``i``, ``em`` и тп.).

    Args:
        soup (BeautifulSoup): Объект beautiful soup.
    """

    style_tags = soup.find_all(STYLE_TAGS_REGEX)
    for tag in style_tags.copy():
        content = _get_tag_text_without_spaces(tag)
        if not content:
            tag.decompose()


def _clean_empty_list_items(soup: BeautifulSoup) -> None:
    """Очищает пустые ``li`` HTML-теги.

    Args:
        soup (BeautifulSoup): Объект beautiful soup.
    """


    tags = soup.find_all("li")
    for tag in tags.copy():
        content = _get_tag_text_without_spaces(tag)
        if not content:
            tag.decompose()


def _get_tag_text_without_spaces(tag: Tag) -> str:
    """Получает из объекта тега текст без пробелов.

    Args:
        tag (Tag): Объект тега.

    Returns:
        str: Текст.
    """

    return re.sub(r"\s", "", tag.get_text())
