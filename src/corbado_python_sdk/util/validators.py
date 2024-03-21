def validate_str_not_empty(v: str) -> str:
    if not v:
        raise ValueError("Name must be at least 3 characters long")
    return v
