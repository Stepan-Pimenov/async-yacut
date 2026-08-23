from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from . import app, db
from .error_handlers import InvalidAPIUsage
from .forms import FileForm, URLForm
from .models import URLMap
from .yandex_disk import async_upload_files


@app.shell_context_processor
def get_shell_context():
    return {'db': db, 'URLMap': URLMap}


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(form.original_link.data, form.custom_id.data)
    except InvalidAPIUsage as error:
        flash(error.message)
        return render_template('index.html', form=form)
    return render_template('index.html', form=form, url_map=url_map)


@app.route('/files', methods=['GET', 'POST'])
async def files_view():
    form = FileForm()
    if not form.validate_on_submit():
        return render_template('files.html', form=form)
    upload_results = await async_upload_files(form.files.data)
    url_maps = []
    for file_name, download_link in upload_results:
        url_maps.append((file_name, URLMap.create(original=download_link)))
    return render_template('files.html', form=form, url_maps=url_maps)


@app.route('/<short>')
def redirect_view(short):
    url_map = URLMap.get_by_short(short)
    if url_map is None:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_map.original)
