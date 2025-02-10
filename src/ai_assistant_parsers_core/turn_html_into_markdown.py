"""Модуль для ``turn_html_into_markdown``."""

import re
import enum

from bs4 import BeautifulSoup
import html2text
from pymarkdown.api import PyMarkdownApi, PyMarkdownApiException


html2text.config.RE_MD_CHARS_MATCHER_ALL = re.compile(r"([`*_{}\[\]()#!~|\-+])")
html2text.config.UNIFIABLE["gt"] = "\\>"


class MarkdownImageStrategy(enum.Enum):
    """Стратегия обработки таблиц."""
    DROP = enum.auto()
    USE_ALT = enum.auto()


class MarkdownTableStrategy(enum.Enum):
    """Стратегия обработки картинок."""
    BYPASS = enum.auto()
    PAD = enum.auto()


def turn_html_into_markdown(
    html: str,
    image_strategy: MarkdownImageStrategy = MarkdownImageStrategy.DROP,
    table_strategy: MarkdownTableStrategy = MarkdownTableStrategy.BYPASS,
    try_fix_markdown: bool = False,
) -> str:
    """Преобразовывает HTML в Markdown.

    Args:
        html (str): HTML-код.
        image_strategy (ImageStrategy, optional): Стратегия обработки картинок. По-умолчанию ImageStrategy.DROP.
        table_strategy (TableStrategy, optional): Стратегия обработки таблиц. По-умолчанию TableStrategy.BYPASS.
        try_fix_markdown (bool, optional): Если `True`, то `pymarkdown` попытается исправить проблемы
            Markdown на выходе.

    Returns:
        str: Markdown.
    """
    html = _prepare_data(html, table_strategy=table_strategy)

    text_maker = html2text.HTML2Text(bodywidth=0)
    text_maker.include_sup_sub = True
    text_maker.escape_snob = True

    text_maker.protect_links = True

    match image_strategy:
        case MarkdownImageStrategy.DROP:
            text_maker.ignore_images = True
        case MarkdownImageStrategy.USE_ALT:
            text_maker.default_image_alt = "image"
            text_maker.images_to_alt = True

    match table_strategy:
        case MarkdownTableStrategy.BYPASS:
            text_maker.bypass_tables = True
        case MarkdownTableStrategy.PAD:
            # https://github.com/Alir3z4/html2text/issues/370
            if not _check_has_nested_table(html):
                text_maker.pad_tables = True
            else:
                text_maker.ignore_tables = True

    markdown = text_maker.handle(html)
    if try_fix_markdown:
        try:
            fixed_result = PyMarkdownApi().fix_string(markdown)
            markdown = fixed_result.fixed_file
        except PyMarkdownApiException as this_exception:
            pass

    return markdown


def _prepare_data(html: str, table_strategy: MarkdownTableStrategy):
    soup = BeautifulSoup(html, "html5lib")

    if table_strategy != MarkdownTableStrategy.BYPASS:
        _add_th_tags_to_all_tables(soup)

    return str(soup)


def _check_has_nested_table(html: str) -> bool:
    soup = BeautifulSoup(html, "html5lib")
    tables = soup.find_all("table")

    for table in tables:
        if table.find_parent("table"):
            return True

    return False


def _add_th_tags_to_all_tables(soup: BeautifulSoup) -> None:
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        if not rows:
            # Пропускаем пустые таблицы, так как в них нет необходимости добавлять заголовки
            continue

        first_row = rows[0]
        # Есть в первой строке нет <th> тега
        if not first_row.find("th"):
            # Находим максимальное количество ячеек в любой строке таблицы.
            # Учитываем и `td`, и `th` для большей гибкости
            max_cells = max(len(row.find_all(["td", "th"])) for row in rows)

            # Создаем новую строку с пустыми заголовками <th>
            new_header_row = soup.new_tag("tr")
            for _ in range(max_cells):
                new_th = soup.new_tag("th")
                new_header_row.append(new_th)

            # Вставляем новую строку с заголовками перед первой строкой таблицы
            first_row.insert_before(new_header_row)
