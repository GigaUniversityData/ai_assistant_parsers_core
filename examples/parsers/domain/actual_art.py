"""
Страницы для теста:
- https://actual-art.spbu.ru/
- https://actual-art.spbu.ru/o-konferentsii/orgkomitet.html
"""

from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


class ActualArtDomainParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=["actual-art.spbu.ru"],
            select_arguments=["#t3-content"],
        )
