import os

import aiofiles
from aiohttp import web


async def get_file(request):
    if 'token' not in request.headers or request.headers['token'] != os.getenv('FS_TOKEN'):
        return web.json_response({"success": False}, status=403)
    response = web.StreamResponse()
    await response.prepare(request)
    async with aiofiles.open("data/" + request.rel_url.query['id'], "rb") as fs:
        await response.write_eof(await fs.read())
    return response
