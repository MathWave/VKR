import os
from os import remove

from aiohttp import web


async def delete_file(request):
    if 'token' not in request.headers or request.headers['token'] != os.getenv('FS_TOKEN'):
        return web.json_response({"success": False}, status=403)
    remove("data/" + request.rel_url.query['id'])
    return web.json_response({"success": True})
