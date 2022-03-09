import asyncio
import json
import sys

from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType
from enum import Enum
from typing import Any, Dict, Optional, List, Callable, Awaitable, TypeVar

from .errors import InvalidToken, InvalidFunction
from .message import Message


__all__ = (
    "Client",
)


class OPCODES(Enum):
    """Discord OP Codes"""

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11

OnT = TypeVar("OnT", bound=Callable[..., Awaitable])

EVENT_CONVERTERS = {
    'MESSAGE_CREATE': Message
}

class Client:
    """
    Represents a discord client that
    handles interactions with the discord
    api in the form of a websocket which
    entails sending websockets, receiving
    events and then dispatching them.
    """

    def __init__(self) -> None:
        self._session: ClientSession
        self._ws: ClientWebSocketResponse
        self._loop = asyncio.AbstractEventLoop
        self._events: Dict[str, Any] = {}

    def on(self, event_name: str) -> Callable[[OnT], OnT]:
        """
        A function used to decorate event
        functions with to declare them
        as an event.

        Parameters
        ----------
        event_name: :class:`str`
            the event to assign the
            function to.
        """

        def decorator(func) -> OnT:
            if not asyncio.iscoroutinefunction(func):
                raise InvalidFunction("Your event must be asynchronous.")
            self._events[event_name] = func
            return func

        return decorator

    async def identify(self, token: str) -> None:
        """
        Sends the IDENTIFY payload to the
        websocket connection to identify
        the client user.
        """
        await self._ws.send_json(
            {
                "op": OPCODES.IDENTIFY.value,
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

    async def _parse_event(self, _message: WSMessage) -> bool:
        """
        Parses an event message.

        Parameters
        ----------
        message: :class:`WSMessage`
            The message passed through.
        """

        try:
            _data = json.loads(_message.data)
        except TypeError:
            print(_message)
            return False

        # print(_data)
        # print("\n\n\n")

        if _message.type is WSMsgType.TEXT and _data["op"] == OPCODES.HEARTBEAT_ACK.value:
            return
        if _message.type is WSMsgType.CLOSED:
            return False
        if _message.type is WSMsgType.TEXT and _data["op"] == OPCODES.HELLO.value:
            self._heartbeat_interval = _data["d"]["heartbeat_interval"] / 1000

        await self.dispatch(_data["t"], _data["d"])
        self._ws.sequence += 1

    async def dispatch(self, _name: str, _raw_data: Dict[Any, Any]) -> None:
        """
        Dispatches the event received from
        the websocket and calls the coroutine
        which has been registered to that
        certain event.

        Parameters
        ----------
        name: :class:`str`
            The name of the event to call.
        data: :class:`Dict[Any, Any]`
            The data passed by the discord
            gateway into the message.
        """

        if _name not in self._events:
            return

        coro = self._events[_name]   

        if _name in EVENT_CONVERTERS:
            data = EVENT_CONVERTERS[_name](_raw_data)
        else:
            data = _raw_data

        await coro(data)

    async def keep_alive(self) -> None:
        """
        Keeps the bot alive which entails
        sending a heartbeat every _ seconds
        to tell the websocket that we're still
        up and running.
        """ 

        while True:
            data = {"op": OPCODES.HEARTBEAT.value, "d": self._ws.sequence}
            await self._ws.send_json(data)
            await asyncio.sleep(self._heartbeat_interval)

    async def start(
        self, token: str, *, session: Optional[ClientSession] = None, loop: Optional[asyncio.AbstractEventLoop] = None
    ) -> None:
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
        self._loop = loop or asyncio.get_running_loop()
        self._ws = await self._session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        self._ws.sequence = 0

        _message = await self._ws.receive()
        await self._parse_event(_message)
        await self.identify(token)

        self._loop.create_task(self.keep_alive())

        async for message in self._ws:
            await self._parse_event(message)
