import asyncio

import aiohttp

from . import app
from .constants import DISK_API_HOST, DISK_API_VERSION, UPLOAD_FOLDER

AUTH_HEADERS = {'Authorization': f'OAuth {app.config["DISK_TOKEN"]}'}
GET_UPLOAD_LINK_URL = (
    f'{DISK_API_HOST}{DISK_API_VERSION}/disk/resources/upload'
)
GET_DOWNLOAD_LINK_URL = (
    f'{DISK_API_HOST}{DISK_API_VERSION}/disk/resources/download'
)


async def async_upload_files(files):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.ensure_future(upload_file_and_get_link(session, file))
            for file in files
        ]
        return await asyncio.gather(*tasks)


async def upload_file_and_get_link(session, file):
    path = f'{UPLOAD_FOLDER}{file.filename}'
    upload_link = await get_upload_link(session, path)
    await put_file(session, upload_link, file.read())
    download_link = await get_download_link(session, path)
    return file.filename, download_link


async def get_upload_link(session, path):
    params = {'path': path, 'overwrite': 'true'}
    async with session.get(
        GET_UPLOAD_LINK_URL, headers=AUTH_HEADERS, params=params
    ) as response:
        response.raise_for_status()
        return (await response.json())['href']


async def put_file(session, upload_link, data):
    async with session.put(upload_link, data=data) as response:
        response.raise_for_status()


async def get_download_link(session, path):
    async with session.get(
        GET_DOWNLOAD_LINK_URL, headers=AUTH_HEADERS, params={'path': path}
    ) as response:
        response.raise_for_status()
        return (await response.json())['href']
