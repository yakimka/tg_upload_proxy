from unittest.mock import Mock

import pytest

from tg_upload_proxy.utils import bot


@pytest.fixture
def mock_tg_credentials(monkeypatch):
    monkeypatch.setenv('TG_API_ID', '12345')
    monkeypatch.setenv('TG_API_HASH', 'my_hash')
    monkeypatch.setenv('TG_BOT_TOKEN', 'my_token')


def test_get_client(monkeypatch, mock_tg_credentials):
    mbot = Mock()
    monkeypatch.setattr(bot, 'TelegramClient', mbot)

    tg_bot = bot.get_bot()

    mbot.assert_called_once_with('bot', 12345, 'my_hash')
    mbot().start.assert_called_once_with(bot_token='my_token')
    assert mbot().start() == tg_bot
