from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, MultipleFileField
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import DataRequired, Optional


class URLForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=[DataRequired(message='Обязательное поле')],
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=[Optional()],
    )
    submit = SubmitField('Создать')


class FileForm(FlaskForm):
    files = MultipleFileField(
        'Выберите файлы',
        validators=[FileRequired(message='Выберите хотя бы один файл')],
    )
    submit = SubmitField('Загрузить')
