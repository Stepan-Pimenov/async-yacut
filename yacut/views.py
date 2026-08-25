from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app
from .constants import REDIRECT_VIEW
from .forms import FileForm, URLForm
from .models import URLMap
from .yandex_disk import async_upload_files


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        return render_template(
            'index.html',
            form=form,
            short_url=URLMap.create(
                form.original_link.data,
                form.custom_id.data,
                validate=False,
            ).get_short_url(),
        )
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('index.html', form=form)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    files = form.files.data
    try:
        download_links = await async_upload_files(files)
    except Exception as error:
        flash(str(error))
        return render_template('files.html', form=form)
    try:
        return render_template(
            'files.html',
            form=form,
            file_links=[(
                file.filename,
                URLMap.create(
                    link, commit=(index == len(download_links) - 1),
                ).get_short_url(),
            ) for index, (file, link) in enumerate(
                zip(files, download_links)
            )],
        )
    except (ValueError, RuntimeError) as error:
        flash(str(error))
        return render_template('files.html', form=form)


@app.route('/<short>', endpoint=REDIRECT_VIEW)
def redirect_view(short):
    if (url_map := URLMap.get(short)) is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
