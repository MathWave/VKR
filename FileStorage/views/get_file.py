import aiofiles
from aiohttp import web


async def get_file(request):
    response = web.StreamResponse()
    await response.prepare(request)
    async with aiofiles.open("data/" + request.rel_url.query['id'], "rb") as fs:
        await response.write_eof(await fs.read())
    return response
