.. AI assistant parsers core documentation master file, created by
   sphinx-quickstart on Wed Sep 11 13:21:19 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AI assistant parsers core
=========================

AI Assistant Parsers Core - это ядро библиотеки, предоставляющее набор общих абстрактных классов и утилит для разработки парсеров,
специализированных под различные высшие учебные заведения (ВУЗы).


Основные компоненты
-------------------
- Абстрактные классы парсеров (``ABCParser``)
- Универсальный парсер (``UniversalParser``)
- Объекты для простой реализации парсеров (``SimpleSelectDomainBaseParser``, ``SimpleFindDomainBaseParser``, ``SimpleSelectPageBaseParser``, ``SimpleFindPageBaseParser``)
- Утилиты для обработки HTML (``clean_one_by_select``, ``clean_all_by_select``, ``rename_all_by_select``, ``convert_tables_to_divs`` и др.)
- Абстрактные классы "Refiners", которые улучшают пост- и пре- обработку HTML
- Универсальные "Refiners" для постобработки (``CleanPostParsingRefiner``, ``RestructurePostParsingRefiner``)
- Утилиты общего назначения (``converts_relative_links_to_absolute``, ``normalize_path``, ``universal_clean_html`` и др.)


Установка
---------
.. code-block:: haskell

   pip install ai_assistant_parsers_core


Требования
-----------
- Python 3.10+


Пример использования:
---------------------
.. code-block:: python

   from bs4 import BeautifulSoup

   from ai_assistant_parsers_core.parsers.utils.clean_blocks import clean_one_by_select
   from ai_assistant_parsers_core.parsers.utils.restructure_blocks import rename_all_by_select
   from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


   class WWWRGUSTDomainParser(SimpleSelectDomainBaseParser):
       """Парсер для сайта ``https://rgust.ru/``"""

       def __init__(self) -> None:
           super().__init__(
               supported_subdomains=["rgust.ru"],  # Парсим страницы, которые не имеют поддомена
               select_arguments=[
                   "section.content",  # Тег, содержащий основной контент
               ],
           )

       def _clean_parsed_html(self, soup: BeautifulSoup) -> None:
           clean_one_by_select(soup, ".breadcrumb")  # Очищаем `.breadcrumb`

       def _restructure_parsed_html(self, soup: BeautifulSoup) -> None:
           rename_all_by_select(soup, "p.main-page-faculty-widget-programs-header", "h2")  # Затем `p` HTML-тег на `h2`


Больше примеров!
----------------
Примеры находятся в папке `examples <https://github.com/GigaUniversity/ai_assistant_parsers_core/tree/main/examples>`_

Основная документация
---------------------
[Ссылка]
