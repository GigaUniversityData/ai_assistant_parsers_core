"""Модуль для ``turn_html_into_markdown``."""

from os import getenv

from aiohttp import ClientSession, ClientConnectorError, ClientResponseError


API_URL = getenv("AAPC__MARKDOWN_API_URL", "http://localhost:8080")


async def turn_html_into_markdown(html: str) -> str:
    """Преобразовывает HTML в Markdown.

    Args:
        html (str): HTML-код.

    Returns:
        str: Markdown.
    """
    async with ClientSession(raise_for_status=True) as client:
        try:
            async with client.post(f"{API_URL}/api/v1/convert", json=dict(html=html)) as response:
                data = await response.json()
        except ClientConnectorError as error:
            raise ServerMarkdownConverterError(f"Cannot connect to markdown api server") from error
        except ClientResponseError as error:
            raise ServerMarkdownConverterError(
                f"Exceptions occurred after receiving a response: "
                f"{error.status} {error.message!r}",
            ) from error

    return data["markdown"]


class MarkdownConverterError(Exception):
    pass


class ServerMarkdownConverterError(MarkdownConverterError):
    pass
