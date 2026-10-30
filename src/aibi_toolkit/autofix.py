"""Automatic naming fixes for semantic-model dumps."""


def fix_measure_name(name: str) -> str:
    """Turn a raw measure name into a display-safe one."""
    from .naming import to_display_name, strip_numbers
    return truncate(to_display_name(strip_numbers(name)), 64)


def truncate(name: str, limit: int = 64) -> str:
    """Truncate without trailing separators."""
    out = name[:limit].rstrip()
    while out and out[-1] in "-_ ":
        out = out[:-1].rstrip()
    return out
