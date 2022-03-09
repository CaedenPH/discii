import asyncio
import sys
import threading

from aiohttp import ClientSession, ClientWebSocketResponse, WSMsgType
from typing import Optional, Dict, Any

from .utils import _to_json
from .errors import InvalidToken


GATEWAY_URL = "wss://gateway.discord.gg/?v=9&encoding=json"


class Client:
    """
    represents a discord client that
    handles interactions with the discord 
    api in the form of a websocket which
    entails sending websockets, receiving 
    events and then dispatching them.
    """

    def __init__(self) -> None:
        self._session: ClientSession
        self._ws: ClientWebSocketResponse
        self._loop = asyncio.AbstractEventLoop

    async def identify(self, token: str) -> None:
        """
        sends the IDENTIFY payload to the
        websocket connection.
        """
        await self._ws.send_str(
            _to_json(
            {
                "op": 2,
                "d": {
                    "token": token,
                    "intents": 513,
                    "properties": {
                        "$os": sys.platform,
                        "$browser": "my_library",
                        "$device": "my_library",
                    },
                },
            }
            )
        )

    async def poll_event(self) -> None:
        """
        Gets an event from the websocket
        """

        _message = await self._ws.receive()
        _message_json = _to_json(_message)
        

        print(_message)
        if _message.type is WSMsgType.CLOSED:
            return False
        print("\n\n\n")

    async def start(self, token: str, *, session: Optional[ClientSession] = None, loop: Optional[asyncio.AbstractEventLoop] = None) -> None:
        """
        Starts the bot.

        Parameters
        ----------
        token: :class:`str`
            The bot token to send the IDENTIFY
            payload with and login.
        session: :class:`Optional[ClientSession]`
            The aiohttp session to use in case
            the user wants to input a pre-existing
            session.
        """

        if not isinstance(token, str) or len(token) != 59:
            raise InvalidToken("Make sure you enter a valid bot token instead of ``{}``".format(token))

        self._session = session or ClientSession()
        self._ws = await self._session.ws_connect(GATEWAY_URL)

        await self.poll_event()
        await self.identify(token) 

        while True:
            status = await self.poll_event()
            if status is False:
                return
























# async def main():
#     session = ClientSession()
#     ws = await session.ws_connect(GATEWAY_URL)
#     await ws.send_str(_to_json(IDENTIFY_PAYLOAD))

#     num = 0
#     while True:
#         msg = await ws.receive()
#         num += 1
#         print(msg)
#         msg_json = json.loads(msg.data)

#         # if num == 4:
#         #     return await session.close()
#         if msg_json["t"] == "GUILD_CREATE":
#             num -= 1
#             continue

#         # print(str(msg_json) + "\n\n\n\n")

#         if msg.type is WSMsgType.CLOSE:
#             print(str(msg) + " :(")
#         if msg.type is WSMsgType.CLOSED:
#             return