from dataclasses import dataclass
from typing import Optional, Type

from aiohttp.web_urldispatcher import View

from tg_upload_proxy.api.view import SendAudioView


@dataclass
class Route:
    method: str
    path: str
    handler: Type[View]
    name: Optional[str] = None


routes = [
    Route('*', '/sendAudio/', SendAudioView)
]
