"""Модуль для ``convert_html_to_markdown``."""

from os import getenv

from aiohttp import ClientSession, ClientConnectorError, ClientResponseError, BasicAuth


API_URL = getenv("AAPC_MARKDOWN_API_URL", "https://uniassistant.ru/api/markdown-converter/convert")
API_AUTH = getenv("AAPC_MARKDOWN_API_AUTH")


async def convert_html_to_markdown(html: str) -> str:
    """Преобразовывает HTML в Markdown.

    Args:
        html (str): HTML-код.

    Returns:
        str: Markdown.
    """
    if API_AUTH is None:
        raise MarkdownConverterError(
            "Authorization parameters are not specified. "
            "Please use the 'AAPC_MARKDOWN_API_AUTH' environment variable for this."
        )
    try:
        login, password = API_AUTH.split(":")
    except ValueError as error:
        raise MarkdownConverterError(
            "'AAPC_MARKDOWN_API_AUTH' environment variable is not valid. "
            "Please use format: [login]:[password]."
        ) from error

    async with ClientSession(raise_for_status=True) as client:
        try:
            async with client.post(
                f"{API_URL}/convert",
                json=dict(html=html),
                auth=BasicAuth(login, password),
            ) as response:
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
