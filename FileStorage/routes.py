from aiohttp import web

from FileStorage.views import get_file, upload_file, delete_file


def setup_routes(app: web.Application):
    app.router.add_get("/get_file", get_file)
    app.router.add_post("/upload_file", upload_file)
    app.router.add_post("/delete_file", delete_file)
