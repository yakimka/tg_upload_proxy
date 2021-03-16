from unittest.mock import ANY, Mock

import pytest

from tg_upload_proxy.utils import bot


@pytest.fixture()
def _mock_tg_credentials(monkeypatch):
    monkeypatch.setenv('TG_API_ID', '12345')
    monkeypatch.setenv('TG_API_HASH', 'my_hash')
    monkeypatch.setenv('TG_BOT_TOKEN', 'my_token')


@pytest.mark.usefixtures('_mock_tg_credentials')
def test_get_client(monkeypatch):
    mbot = Mock()
    monkeypatch.setattr(bot, 'TelegramClient', mbot)

    tg_bot = bot.get_bot()

    mbot.assert_called_once_with(ANY, 12345, 'my_hash')
    mbot().start.assert_called_once_with(bot_token='my_token')  # noqa: S106
    assert mbot().start() == tg_bot
