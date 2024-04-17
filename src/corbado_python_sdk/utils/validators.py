def validate_str_not_empty(v: str) -> str:
    """Validates that str is not empty

    Args:
        v (str): validated object

    Raises:
        ValueError: if string is empty

    Returns:
        str: validated string
    """
    if not v:
        raise ValueError("Name must be at least 3 characters long")
    return v
