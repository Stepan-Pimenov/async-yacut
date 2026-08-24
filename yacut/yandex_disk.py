import asyncio

import aiohttp

from settings import Config

AUTH_HEADERS = {'Authorization': f'OAuth {Config.DISK_TOKEN}'}
GET_UPLOAD_LINK_URL = (
    f'{Config.DISK_API_HOST}{Config.DISK_API_VERSION}/disk/resources/upload'
)
GET_DOWNLOAD_LINK_URL = (
    f'{Config.DISK_API_HOST}{Config.DISK_API_VERSION}/disk/resources/download'
)


async def async_upload_files(files):
    async with aiohttp.ClientSession() as session:
        return await asyncio.gather(*[
            asyncio.ensure_future(upload_file_and_get_link(session, file))
            for file in files
        ])


async def upload_file_and_get_link(session, file):
    path = 'app:/' + file.filename
    upload_link = await get_upload_link(session, path)
    await put_file(session, upload_link, file.read())
    return await get_download_link(session, path)


async def get_upload_link(session, path):
    async with session.get(
        GET_UPLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': path, 'overwrite': 'true'},
    ) as response:
        response.raise_for_status()
        return (await response.json())['href']


async def put_file(session, upload_link, data):
    async with session.put(upload_link, data=data) as response:
        response.raise_for_status()


async def get_download_link(session, path):
    async with session.get(
        GET_DOWNLOAD_LINK_URL,
        headers=AUTH_HEADERS,
        params={'path': path},
    ) as response:
        response.raise_for_status()
        return (await response.json())['href']
