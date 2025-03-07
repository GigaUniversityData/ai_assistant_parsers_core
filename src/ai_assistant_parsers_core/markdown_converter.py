"""Модуль для ``convert_html_to_markdown``."""

from os import getenv

from aiohttp import ClientSession, ClientConnectorError, ClientResponseError, BasicAuth


API_URL = getenv("AAPC_MARKDOWN_API_URL", "http://5.35.3.148:16000")
API_AUTH = getenv("AAPC_MARKDOWN_API_AUTH")


async def convert_html_to_markdown(html: str) -> str:
    """Преобразовывает HTML в Markdown.

    Args:
        html (str): HTML-код.

    Returns:
        str: Markdown.
    """
    if API_AUTH is None:
        raise InvalidAuthorizationError(
            "Authorization parameters are not specified. "
            "Please use the 'AAPC_MARKDOWN_API_AUTH' environment variable for this"
        )
    try:
        login, password = API_AUTH.split(":")
    except ValueError as error:
        raise InvalidAuthorizationError(
            "'AAPC_MARKDOWN_API_AUTH' environment variable is not valid. "
            "Please use format: [login]:[password]"
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
            raise ServerConnectionError from error
        except ClientResponseError as error:
            raise ServerResponseError from error

    return data["markdown"]


class MarkdownConverterError(Exception):
    pass


class ServerConnectionError(MarkdownConverterError):
    def __str__(self) -> str:
        return "Cannot connect to MarkdownAPI server"


class ServerResponseError(MarkdownConverterError):
    pass


class InvalidAuthorizationError(MarkdownConverterError):
    pass
