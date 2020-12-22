from http import HTTPStatus

from aiohttp import web
from aiohttp.web_urldispatcher import View
from aiohttp_apispec import (docs, request_schema, response_schema)
from telethon import utils
from telethon.tl.types import DocumentAttributeAudio

from tg_upload_proxy.api.schema import SendAudio, SendAudioResponse
from tg_upload_proxy.utils.bot import get_bot


class SendAudioView(View):
    @docs(summary='Send audio')
    @request_schema(SendAudio())
    @response_schema(SendAudioResponse(), code=HTTPStatus.OK)
    async def post(self):
        data = self.request['data']
        attributes = [DocumentAttributeAudio(
            duration=data.pop('duration'),
            title=data.pop('title'),
            performer=data.pop('performer')
        )]

        bot = await get_bot()
        async with bot:
            res = await bot.send_file(
                entity=data['chat_id'],
                file=data['audio'],
                caption=data.get('caption'),
                parse_mode=data.get('parse_mode'),
                thumb=data['thumb'],
                reply_to=data['reply_to_message_id'],
                attributes=attributes
            )

        if res.media is None:
            return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, text='Upload error')

        file_id = utils.pack_bot_file_id(res.media.document)

        if file_id is None:
            return web.Response(status=HTTPStatus.INTERNAL_SERVER_ERROR, text='ID encoding error')

        return web.json_response({'file_id': file_id})
