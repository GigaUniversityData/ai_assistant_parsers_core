"""
Страницы для теста:
- https://kantiana.ru/tor/#
- https://kantiana.ru/universitys/#
- https://kantiana.ru/enrollee/#
- https://kantiana.ru/students/fk-baltika-bfu-im-i-kanta/#
"""

from bs4 import BeautifulSoup

from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select
from ai_assistant_parsers_core.parsers.utils.restructure_blocks import rename_all_by_select
from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


class MainWWWDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["kantiana.ru"],
            select_arguments=[".page"],
            excluded_paths=["/enrollee/programs/*?"],
        )

    def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
        clean_one_by_select(soup, ".banner")  # Банер
        clean_one_by_select(soup, ".section--news")  # Новости

    def _restructure_parsed_html(self, soup: BeautifulSoup) -> None:
        # Заголовки #
        rename_all_by_select(soup, "p.prog-section__title", "h2")  # Старый тег
        rename_all_by_select(soup, "div.prog-section__title", "h2")
        rename_all_by_select(soup, "div.career__title", "h4")
        rename_all_by_select(soup, "div.banner-news__title", "h2")
        rename_all_by_select(soup, "div.banner__title", "h2")
        rename_all_by_select(soup, "div.rounded-block__title", "h2")
        rename_all_by_select(soup, "div.paragraph__title", "h2")
        rename_all_by_select(soup, "p.sidebar-block__title", "h2")
        rename_all_by_select(soup, "div.sidebar-block__title ", "h2")
        rename_all_by_select(soup, "p.section__title", "h2")
        rename_all_by_select(soup, "h3.section__title", "h2")
        rename_all_by_select(soup, "div.quote__title", "h2")
        rename_all_by_select(soup, "h3.form-boxed__title", "h2")

        # Подзаголовки #
        rename_all_by_select(soup, "p.prog-section__subtitle", "h3")
        rename_all_by_select(soup, "p.contacts__subtitle", "h3")

        # Классы h* #
        rename_all_by_select(soup, ".h2", "h2")
        rename_all_by_select(soup, ".h3", "h2")
        rename_all_by_select(soup, ".h4", "h2")  # Не используется на сайте
        rename_all_by_select(soup, ".h5", "h2")

        # Теги стиля #
        # Часто является заголовком, но есть исключения, так как это больше тег стиля
        rename_all_by_select(soup, "p.text-blue", "h2")
        # Является тегом заголовка для https://kantiana.ru/students/scholarship/*
        rename_all_by_select(soup, "p.text-sky-blue", "h2")
        # Часто является заголовком или подзаголовком, но есть исключения, так как это больше тег стиля
        rename_all_by_select(soup, "p.text-important", "h2")

        # Особые теги #
        rename_all_by_select(soup, "div.review_name", "h3")
        rename_all_by_select(soup, "p.career__heading", "h5")
        rename_all_by_select(soup, "div.prog__block--title", "h3")
        rename_all_by_select(soup, ".vikon-wrapper #vikon-content h4.vikon-title-block", "h2")
