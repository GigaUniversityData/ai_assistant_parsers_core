from __future__ import annotations


class PageMixin():
    def __init__(
        self,
        supported_urls: list[str],
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self._supported_urls = supported_urls

    def check(self, url: str) -> bool:
        return url in self._supported_urls
