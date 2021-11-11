from aiohttp import web

from FileStorage.sync import write_meta
import aiofiles


async def upload_file(request):
    file_id = await write_meta(request)
    async with aiofiles.open("data/" + str(file_id), "wb") as fs:
        await fs.write(await request.content.read())
    return web.json_response({"id": file_id})
