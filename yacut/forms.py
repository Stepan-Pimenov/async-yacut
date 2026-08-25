from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, Optional, Regexp

from .constants import ORIGINAL_MAX_LENGTH, SHORT_MAX_LENGTH, SHORT_PATTERN

ORIGINAL_LABEL = 'Длинная ссылка'
CUSTOM_ID_LABEL = 'Ваш вариант короткой ссылки'
SUBMIT_LABEL = 'Создать'
FILES_LABEL = 'Выберите файлы'
UPLOAD_LABEL = 'Загрузить'
REQUIRED_MESSAGE = 'Обязательное поле'
LONG_ORIGINAL_MESSAGE = (
    f'Максимальная длина ссылки в символах - {ORIGINAL_MAX_LENGTH}'
)
LONG_SHORT_MESSAGE = f'Максимальная длина в символах - {SHORT_MAX_LENGTH}'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
FILES_REQUIRED_MESSAGE = 'Выберите хотя бы один файл'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_MESSAGE),
            Length(max=ORIGINAL_MAX_LENGTH, message=LONG_ORIGINAL_MESSAGE),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Optional(),
            Length(max=SHORT_MAX_LENGTH, message=LONG_SHORT_MESSAGE),
            Regexp(SHORT_PATTERN, message=INVALID_SHORT_MESSAGE),
        ],
    )
    submit = SubmitField(SUBMIT_LABEL)


class FileForm(FlaskForm):
    files = MultipleFileField(
        FILES_LABEL,
        validators=[FileRequired(message=FILES_REQUIRED_MESSAGE)],
    )
    submit = SubmitField(UPLOAD_LABEL)
