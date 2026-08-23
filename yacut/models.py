from datetime import datetime, timezone
from random import choices

from flask import url_for

from . import db
from .constants import (
    ALLOWED_CHARS,
    DUPLICATE_SHORT_ID_MESSAGE,
    INVALID_SHORT_ID_MESSAGE,
    RESERVED_SHORT_IDS,
    SHORT_ID_LENGTH,
    SHORT_ID_MAX_LENGTH,
)
from .error_handlers import InvalidAPIUsage
from .utils import is_short_id_format_valid


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(
        db.String(SHORT_ID_MAX_LENGTH), unique=True, nullable=False
    )
    timestamp = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view', short=self.short, _external=True
            ),
        )

    @classmethod
    def get_by_short(cls, short):
        return cls.query.filter_by(short=short).first()

    @classmethod
    def is_short_id_available(cls, short):
        return (
            short not in RESERVED_SHORT_IDS
            and cls.get_by_short(short) is None
        )

    @classmethod
    def get_unique_short_id(cls):
        while True:
            short = ''.join(choices(ALLOWED_CHARS, k=SHORT_ID_LENGTH))
            if cls.is_short_id_available(short):
                return short

    @classmethod
    def create(cls, original, short=None):
        if short:
            if not is_short_id_format_valid(short):
                raise InvalidAPIUsage(INVALID_SHORT_ID_MESSAGE)
            if not cls.is_short_id_available(short):
                raise InvalidAPIUsage(DUPLICATE_SHORT_ID_MESSAGE)
        else:
            short = cls.get_unique_short_id()
        url_map = cls(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map
