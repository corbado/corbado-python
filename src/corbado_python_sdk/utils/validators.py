from urllib import parse


def url_validator(url: str) -> str:
    """Url validator.

    Args:
        url (str): URL.

    Raises:
        ValueError: Raises ValueError if url is not valid.

    Returns:
        str: validated url.
    """
    try:
        parts: parse.ParseResult = parse.urlparse(url)
    except ValueError:
        raise ValueError("Assert failed: parse_url() returned error")

    if parts.scheme != "https":
        raise ValueError("Assert failed: scheme needs to be https")

    if not parts.hostname:
        raise ValueError("Assert failed: host is empty")

    if parts.username:
        raise ValueError("Assert failed: username needs to be empty")

    if parts.path:
        raise ValueError("Assert failed: path needs to be empty")

    if parts.password:
        raise ValueError("Assert failed: password needs to be empty")

    if parts.query:
        raise ValueError("Assert failed: querystring needs to be empty")

    if parts.fragment:
        raise ValueError("Assert failed: fragment needs to be empty")
    return url
