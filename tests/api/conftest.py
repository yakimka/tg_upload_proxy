import pytest

from tg_upload_proxy.api.__main__ import parser
from tg_upload_proxy.api.app import create_app


@pytest.fixture()
def arguments(aiomisc_unused_port):
    """
    Аргументы для запуска приложения.
    """
    return parser.parse_args(
        [
            '--log-level=debug',
            '--api-address=127.0.0.1',
            f'--api-port={aiomisc_unused_port}',
        ]
    )


@pytest.fixture()
async def api_client(aiohttp_client, arguments):
    app = create_app()
    client = await aiohttp_client(app, server_kwargs={
        'port': arguments.api_port
    })

    try:
        yield client
    finally:
        await client.close()
