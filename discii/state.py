from __future__ import annotations

from asyncio import AbstractEventLoop, get_running_loop
from aiohttp import ClientSession, ClientWebSocketResponse

from .http import HTTPClient


class ClientState:
    _session: ClientSession
    _loop: AbstractEventLoop
    _ws: ClientWebSocketResponse
    _http: HTTPClient

    @classmethod
    async def new(cls, token: str, *, session: ClientSession = None, loop: AbstractEventLoop = None) -> ClientState:
        self = cls()
        self._session = session or ClientSession()
        self._http = HTTPClient(token, session=self._session)
        self._loop = loop or get_running_loop()
        self._ws = await self._session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        self._ws.sequence = 0
        
        return self
