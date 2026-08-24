import re
from datetime import datetime
from random import choices

from . import db
from .constants import (
    ALLOWED_CHARS,
    GENERATION_ATTEMPTS,
    ORIGINAL_MAX_LENGTH,
    RESERVED_SHORTS,
    SHORT_LENGTH,
    SHORT_MAX_LENGTH,
    SHORT_PATTERN,
)

INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
DUPLICATE_SHORT_MESSAGE = (
    'Предложенный вариант короткой ссылки уже существует.'
)
LONG_ORIGINAL_MESSAGE = 'Слишком длинная ссылка.'
NO_UNIQUE_SHORT_MESSAGE = 'Не удалось подобрать уникальную короткую ссылку.'


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(SHORT_MAX_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def get(short):
        return URLMap.query.filter_by(short=short).first()

    @staticmethod
    def is_short_valid(short):
        return (
            len(short) <= SHORT_MAX_LENGTH
            and re.match(SHORT_PATTERN, short)
        )

    @staticmethod
    def get_unique_short():
        for _ in range(GENERATION_ATTEMPTS):
            short = ''.join(choices(ALLOWED_CHARS, k=SHORT_LENGTH))
            if URLMap.get(short) is None:
                return short
        raise ValueError(NO_UNIQUE_SHORT_MESSAGE)

    @staticmethod
    def create(original, short=None, validate=True, commit=True):
        if validate and len(original) > ORIGINAL_MAX_LENGTH:
            raise ValueError(LONG_ORIGINAL_MESSAGE)
        if short:
            if validate and not URLMap.is_short_valid(short):
                raise ValueError(INVALID_SHORT_MESSAGE)
            if short in RESERVED_SHORTS or URLMap.get(short) is not None:
                raise ValueError(DUPLICATE_SHORT_MESSAGE)
        else:
            short = URLMap.get_unique_short()
        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        if commit:
            db.session.commit()
        return url_map
