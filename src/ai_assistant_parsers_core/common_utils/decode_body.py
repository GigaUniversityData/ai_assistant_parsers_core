from contextlib import suppress

import charset_normalizer


def decode_body(byte_string: bytes) -> str:
    with suppress(UnicodeDecodeError):
        return byte_string.decode()

    with suppress(UnicodeDecodeError):
        return byte_string.decode(encoding="windows-1251")

    result = charset_normalizer.detect(byte_string)
    if result["encoding"] is not None:
        return byte_string.decode(encoding=result["encoding"])

    raise RuntimeError("The encoding could not be detected automatically")
