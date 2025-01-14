"""
Страницы для теста:
- https://kantiana.ru/enrollee/programs/iskusstvennyy-intellekt-i-analiz-dannykh/#
- https://kantiana.ru/enrollee/programs/informatika-i-programmirovanie/#
- https://kantiana.ru/enrollee/programs/bioinzheneriya-i-bioinformatika/#
- https://kantiana.ru/enrollee/programs/mashinostroenie/#
"""

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.magic_url import MagicURL
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser
from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select, clean_all_by_select
from ai_assistant_parsers_core.parsers.utils.restructure_blocks import rename_all_by_select, rename_one_by_select


class ProgramsWWWDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["kantiana.ru"],
            select_arguments=[".page"],
            included_paths=["/enrollee/programs/*?"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        clean_one_by_select(soup, ".section:has(> .container > .breadcrumbs)")  # Breadcrumbs

        clean_one_by_select(soup, ".prog_forma > .col-send-doc")  # "Приёмная комиссия"

        clean_one_by_select(soup, ".section--links")  # Секция дополнительных ссылок
        clean_one_by_select(soup, ".section--news")  # Секция новостей
        clean_one_by_select(soup, ".section--programm-courses")  # Долгосрочные курсы подготовки для абитуриентов 2024

        clean_all_by_select(soup, ".discipline-type")  # Тип программы обучения

    # TODO: Создать методы для упрощения кода
    def _restructure_parsed_html(self, soup: BeautifulSoup, magic_url: MagicURL) -> None:
        # Глобальные #

        rename_all_by_select(soup, "p.text-important", "h2")

        rename_all_by_select(soup, ".prog-section__title", "h2")  # Заголовки секции программы
        rename_all_by_select(soup, ".prog-section__subtitle", "h3")  # Подзаголовки секции программы

        rename_all_by_select(soup, "div.rounded-block__title", "h2")  # Заголовки круглых блоков
        rename_all_by_select(soup, "div.rounded-block__subtitle", "h3")  # Подзаголовки круглых блоков
        for tag in soup.select("h3.rounded-block__subtitle"):
            tag.string = tag.get_text().strip()

        rename_all_by_select(soup, ".review_name", "h3")  # Имена тех, кто оставил отзывы

        rename_all_by_select(soup, ".career__title", "h4")  # Заголовок карьеры
        rename_all_by_select(soup, ".career__heading", "h5")  # Подзаголовки карьеры
        clean_all_by_select(soup, ".career__subtitle")  # ''Подзаголовок'' карьеры (Всегда имеет контент "Должность")

        # Блоки с номерами
        clean_all_by_select(soup, ".number__info")  # JS-кнопка для открытия дополнительной информации
        rename_all_by_select(soup, ".number__value", "span")
        rename_all_by_select(soup, ".number__title", "span")
        for tag in soup.select(".number__title"):
            text = tag.get_text()
            tag.string = text[0].lower() + text[1:]

        # Общие #

        # О программе
        if (tag := soup.select_one(".prog_forma")) is not None:
            tag.insert(0, BeautifulSoup(f"<h2>О программе</h2>", "html.parser"))

        # TODO?: Сделать не в списке
        # Предлагаемая квалификация
        if (tag := soup.select_one(".prog__number > .number__text > p")) is not None:
            tag.name = "span"
            tag.string = f"{tag.string.strip()}: "

        # При поддержке
        if (tag := soup.select_one(".prog__in-connection")) is not None:
            tag.insert(0, BeautifulSoup(f"<h2>При поддержке</h2>", "html.parser"))

        # Форма обучения программы
        if (tag := soup.select_one(".prog_forma > ul.nav-pills > li")) is not None:
            tag.insert(0, BeautifulSoup(f"<span>Форма обучения: </span>", "html.parser"))

        rename_one_by_select(soup, ".prog_forma > ul.nav-pills > li > button", "span")
        rename_one_by_select(soup, ".prog_forma > ul.nav-pills > li", "div")
        rename_one_by_select(soup, ".prog_forma > ul.nav-pills", "div")

        # Контакты программы
        if (tag := soup.select_one(".prog__contacts")) is not None:
            tag.insert(0, BeautifulSoup(f"<h2>Контакты</h2>", "html.parser"))

        # Позиция менеджера
        if (tag := soup.select_one(".manager__position")) is not None:
            tag.name = "span"
            tag.string = f" ({tag.string})"

        # Факультет
        if (tag := soup.select_one(".col--faculty")) is not None:
            tag.insert(0, BeautifulSoup(f"<span>Факультет: </span>", "html.parser"))

        # Год обучения в "Программа обучения"
        rename_all_by_select(soup, ".prog__block--title", "h3")

        # Программы обучения
        rename_all_by_select(soup, ".prog-block__wrapper > div.row", "ul")
        rename_all_by_select(soup, ".prog-block__wrapper > .row > div", "li")

        # Отметка фундаментальных дисциплин
        for tag in soup.select(".prog__block--fundamental:not(.prog__block--title)"):
            tag.append(BeautifulSoup(f"<span> (фундаментальная дисциплина)</span>", "html.parser"))
        rename_all_by_select(soup, ".prog__block--fundamental:not(.prog__block--title)", "span")

        # Отметка прикладных дисциплин
        for tag in soup.select(".prog__block--pract:not(.prog__block--title)"):
            tag.append(BeautifulSoup(f"<span> (прикладная дисциплина)</span>", "html.parser"))
        rename_all_by_select(soup, ".prog__block--pract:not(.prog__block--title)", "span")
