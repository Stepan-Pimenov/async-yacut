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
LONG_ORIGINAL_MESSAGE = 'Максимальная длина ссылки - {} символов'
LONG_SHORT_MESSAGE = 'Максимальная длина - {} символов'
INVALID_SHORT_MESSAGE = 'Указано недопустимое имя для короткой ссылки'
FILES_REQUIRED_MESSAGE = 'Выберите хотя бы один файл'


class URLForm(FlaskForm):
    original_link = URLField(
        ORIGINAL_LABEL,
        validators=[
            DataRequired(message=REQUIRED_MESSAGE),
            Length(
                max=ORIGINAL_MAX_LENGTH,
                message=LONG_ORIGINAL_MESSAGE.format(ORIGINAL_MAX_LENGTH),
            ),
        ],
    )
    custom_id = StringField(
        CUSTOM_ID_LABEL,
        validators=[
            Optional(),
            Length(
                max=SHORT_MAX_LENGTH,
                message=LONG_SHORT_MESSAGE.format(SHORT_MAX_LENGTH),
            ),
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
