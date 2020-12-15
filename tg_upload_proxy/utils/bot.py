import os

from telethon import TelegramClient
from telethon.sessions import MemorySession


def get_bot():
    tg_api_id = int(os.environ['TG_API_ID'])
    tg_api_hash = os.environ['TG_API_HASH']
    tg_bot_token = os.environ['TG_BOT_TOKEN']

    client = TelegramClient(MemorySession(), tg_api_id, tg_api_hash)
    return client.start(bot_token=tg_bot_token)
