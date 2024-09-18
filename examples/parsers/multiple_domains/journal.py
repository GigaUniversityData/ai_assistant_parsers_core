from ai_assistant_parsers_core.parsers import SimpleSelectDomainBaseParser


_ALLOWED_SUPPORTED_SUBDOMAINS = [
    "aasjournal.spbu.ru",
    "applmathjournal.spbu.ru",
    "artsjournal.spbu.ru",
    "escjournal.spbu.ru",
    "history-journal.spbu.ru",
    "biocomm.spbu.ru",
    "economicsjournal.spbu.ru",
    "politex.spbu.ru",
    "pravovedenie.spbu.ru",
    "rjm.spbu.ru",
]


class JournalParser(SimpleSelectDomainBaseParser):
    def __init__(self) -> None:
        super().__init__(
            allowed_domains_paths=_ALLOWED_SUPPORTED_SUBDOMAINS,
            select_arguments=[".pkp_structure_main"],
        )
