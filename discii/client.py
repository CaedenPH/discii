import asyncio
import json
import sys

from aiohttp import ClientSession, ClientWebSocketResponse, WSMessage, WSMsgType
from typing import Any, Coroutine, Dict, Optional, List, Callable, Awaitable, TypeVar, TYPE_CHECKING

from .errors import InvalidToken, InvalidFunction
from .gateway import OPCODES, Route
from .message import Message
from .state import ClientState


__all__ = ("Client",)


OnT = TypeVar("OnT", bound=Callable[..., Awaitable])

EVENT_CONVERTERS = {
    "READY": None,
    "MESSAGE_CREATE": Message,
}


class Client:
    """
    Represents a discord client that
    handles interactions with the discord
    api in the form of a websocket which
    entails sending websockets, receiving
    events and then dispatching them.

    Attributes
    ----------
    _session: :class:`ClientSession`
        The aiohttp session used to handle
        the websocket interactions.
    _ws: :class:`ClientWebSocketResponse`
        The websocket that handles all interactions
        with the discord api.
    _loop: :class:`asyncio.AbstractEventLoop`
        The Event Loop used to run all tasks
        from.
    """

    def __init__(self) -> None:
        self._state: ClientState
        self._session: ClientSession
        self._ws: ClientWebSocketResponse
        self._loop: asyncio.AbstractEventLoop
        self._events: Dict[str, List[OnT]] = {}

    def on(self, event_name: str, *, raw: bool = False) -> Callable[[OnT], OnT]:
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

        def decorator(func: Callable[..., Coroutine[Any, Any, Any]]) -> OnT:
            if not asyncio.iscoroutinefunction(func):
                raise InvalidFunction("Your event must be asynchronous.")

            func._raw = raw
            if event_name in self._events:
                self._events[event_name].append(func)
            else:
                self._events[event_name] = [func]
            return func

        return decorator

    async def identify(self, token: str) -> None:
        """
        Sends the IDENTIFY payload to the
        websocket connection to identify
        the client user.

        Parameters
        ----------
        token: :class:`str`
            The bot token used to identify
            in the payload.
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

    async def _parse_message(self, _message: WSMessage) -> bool:
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

        if _message.type is WSMsgType.CLOSED:
            return False

        if _message.type is WSMsgType.TEXT and _data["op"] == OPCODES.HEARTBEAT_ACK.value:
            return

        if _message.type is WSMsgType.TEXT and _data["op"] == OPCODES.HELLO.value:
            self._heartbeat_interval = _data["d"]["heartbeat_interval"] / 1000

        self._ws.sequence += 1
        await self.dispatch(_data["t"], _data["d"])

    async def _run_event(self, coro: Callable[..., Coroutine[Any, Any, Any]], *args: Any) -> None:
        """
        Runs the event within a task.

        Parameters
        ----------
        coro: :class:`Callable[..., Coroutine[Any, Any, Any]]`
            The coroutine to run.
        args: :class:`Any`
            The args to pass into the
            event function.
        """

        try:
            if args[0] is None:
                await coro()
            else:
                await coro(*args)
        except Exception as e:
            print("Yikes... " + str(e))

    async def dispatch(self, _event_name: str, _raw_data: Dict[Any, Any]) -> None:
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

        if _event_name not in self._events:
            return
        for coro in self._events[_event_name]:
            if coro._raw:
                data = _raw_data
            else:
                converter = EVENT_CONVERTERS[_event_name]
                if converter is None:
                    data = None
                else:
                    data = converter(self._state, _raw_data)

            self._loop.create_task(self._run_event(coro, data))

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

        self._state = await ClientState.new(token)
        self._session = self._state._session
        self._loop = self._state._loop
        self._ws = self._state._ws

        # _message = await self._ws.receive()
        # await self._parse_message(_message)
        await self.identify(token)

        self._loop.create_task(self.keep_alive())

        async for message in self._ws:
            await self._parse_message(message)

    async def send(self) -> None:
        r = Route("POST", "/channels/{channel_id}/messages".format(channel_id=942553598166978581))
        await self._state._http.request(r, json={"content": "hi"})
