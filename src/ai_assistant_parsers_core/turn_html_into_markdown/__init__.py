"""Модуль для ``turn_html_into_markdown``."""

from os import getenv


SERVER_URL = "http://localhost:8080"

API_URL = getenv("AAPC__MARKDOWN_API_URL", "http://localhost:8080")


async def turn_html_into_markdown(html: str) -> str:
    """Преобразовывает HTML в Markdown.

    Args:
        html (str): HTML-код.

    Returns:
        str: Markdown.
    """
    async with ClientSession() as client:
        async with client.post(f"{SERVER_URL}/api/v1/convert", json=dict(html=html)) as response:
            if response.status != 200:
                # TODO: Handle server closed errors.
                raise ServerMarkdownConverterError(f"Ошибка на стороне сервера. Код ошибки: {response.status}.")
            data = await response.json()

    return data["markdown"]


class MarkdownConverterError(Exception):
    pass


class ServerMarkdownConverterError(Exception):
    pass
