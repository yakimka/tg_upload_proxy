import dataclasses
import logging

from aiohttp import web
from aiohttp.web_middlewares import normalize_path_middleware
from aiohttp_apispec import (setup_aiohttp_apispec, validation_middleware)

from tg_upload_proxy.api import urls

MEGABYTE = 1024 ** 2
MAX_REQUEST_SIZE = 300 * MEGABYTE

log = logging.getLogger(__name__)


def create_app() -> web.Application:
    app = web.Application(
        client_max_size=MAX_REQUEST_SIZE,
        middlewares=[validation_middleware, normalize_path_middleware()]
    )

    # Registering routes
    for route in urls.routes:
        log.debug('Registering route %r', route)
        app.router.add_route(**dataclasses.asdict(route))

    # Swagger docs on /docs/ url
    setup_aiohttp_apispec(
        app=app,
        title='TG File Uploader API',
        version='v1',
        swagger_path='/docs/'
    )

    return app
