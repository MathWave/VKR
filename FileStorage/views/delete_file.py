import os
from os import remove

from aiohttp import web


async def delete_file(request):
    remove("data/" + request.rel_url.query['id'])
    return web.json_response({"success": True})
