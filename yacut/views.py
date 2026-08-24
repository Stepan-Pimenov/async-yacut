from http import HTTPStatus

import aiohttp
from flask import abort, flash, redirect, render_template, url_for

from . import app
from .constants import REDIRECT_VIEW
from .forms import FileForm, URLForm
from .models import URLMap
from .yandex_disk import async_upload_files

UPLOAD_ERROR_MESSAGE = 'Не удалось загрузить файлы. Попробуйте позже.'


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        short = URLMap.create(
            form.original_link.data, form.custom_id.data, validate=False
        ).short
    except ValueError as error:
        flash(str(error))
        return render_template('index.html', form=form)
    short_url = url_for(REDIRECT_VIEW, short=short, _external=True)
    return render_template('index.html', form=form, short_url=short_url)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    try:
        download_links = await async_upload_files(files)
    except aiohttp.ClientError:
        flash(UPLOAD_ERROR_MESSAGE)
        return render_template('files.html', form=form)
    last = len(download_links) - 1
    url_maps = [
        URLMap.create(link, validate=False, commit=(index == last))
        for index, link in enumerate(download_links)
    ]
    file_links = [
        (
            file.filename,
            url_for(REDIRECT_VIEW, short=url_map.short, _external=True),
        )
        for file, url_map in zip(files, url_maps)
    ]
    return render_template('files.html', form=form, file_links=file_links)


@app.route('/<short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    if (url_map := URLMap.get(short)) is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
