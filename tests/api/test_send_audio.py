from http import HTTPStatus
from unittest.mock import AsyncMock, patch

import pytest

from tg_upload_proxy.api import view


@pytest.fixture()
def mock_get_bot(monkeypatch):
    mock_get_bot_ = AsyncMock()
    monkeypatch.setattr(view, 'get_bot', mock_get_bot_)
    return mock_get_bot_


async def test_missing_fields(mock_get_bot, api_client):
    response = await api_client.post('/sendAudio/')
    data = await response.json()

    expected = {
        'chat_id': ['Missing data for required field.'],
        'audio': ['Missing data for required field.'],
    }
    assert expected == data


@pytest.fixture
def request_data():
    return {
        'chat_id': 100123,
        'audio': 'http://audio.file',
    }


@patch('tg_upload_proxy.api.view.utils.pack_bot_file_id')
async def test_send_audio(mock_pack_bot_file_id, mock_get_bot, api_client, request_data):
    mock_pack_bot_file_id.return_value = 'audio_file_id'
    response = await api_client.post('/sendAudio/', data=request_data)
    data = await response.json()

    assert HTTPStatus.OK == response.status
    assert 'audio_file_id' == data['file_id']


@patch('tg_upload_proxy.api.view.utils.pack_bot_file_id')
async def test_file_id_not_encoded(mock_pack_bot_file_id, mock_get_bot, api_client, request_data):
    mock_pack_bot_file_id.return_value = None
    response = await api_client.post('/sendAudio/', data=request_data)

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status
    assert 'ID encoding error' == await response.text()


async def test_send_file_error(mock_get_bot, api_client, request_data):
    mock_get_bot.return_value.send_file.side_effect = Exception('Oops...')

    response = await api_client.post('/sendAudio/', data=request_data)

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status
    assert 'Oops...' == await response.text()


async def test_empty_media(mock_get_bot, api_client, request_data):
    mock_get_bot.return_value.send_file.return_value.media = None

    response = await api_client.post('/sendAudio/', data=request_data)

    assert HTTPStatus.INTERNAL_SERVER_ERROR == response.status
    assert 'Upload error' == await response.text()
