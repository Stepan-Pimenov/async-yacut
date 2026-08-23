import re

from .constants import SHORT_ID_MAX_LENGTH, SHORT_ID_PATTERN


def is_short_id_format_valid(short_id):
    return (
        len(short_id) <= SHORT_ID_MAX_LENGTH
        and re.match(SHORT_ID_PATTERN, short_id) is not None
    )
