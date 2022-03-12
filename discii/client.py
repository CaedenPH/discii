import asyncio
from typing import Any, Dict, List, TypeVar, Callable, Coroutine

from aiohttp import ClientSession

from .errors import InvalidBotToken, InvalidFunction
from .gateway import DiscordWebSocket
from .http import HTTPClient

# fmt: off
__all__ = (
    'Client',
)
# fmt: on


Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


class Client:
    """
    Represents a Client that interacts with
    the discord api and manages websocket connections.

    Attributes
    ----------
    loop: :class:`AbstractEventLoop`
        The loop to run all tasks and asynchronous
        coroutines run from.
    http: :class:`HTTPClient`
        The client which manages all interactions
        with the discord api.
    ws: :class:`DiscordWebSocket`
        The websocket to manage the gateway with
        the discord api.
    """

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop
        self.http: HTTPClient
        self.ws: DiscordWebSocket

        self.events: Dict[str, List[Callable[..., Coroutine[Any, Any, Any]]]] = {}

    def on(self, event_name: str, *, raw: bool = False):
        """
        Registers a coroutine as an event.

        Parameters
        ----------
        event_name: :class:`str`
            The event name to receive events from.
        raw: :class:`bool`
            Whether or not to pass the raw data received
            from the event.
        """

        def inner(func: Coro) -> Coro:
            if not asyncio.iscoroutinefunction(func):
                raise InvalidFunction("Your event must be a coroutine.")

            if event_name in self.events:
                self.events[event_name].append(func)
            else:
                self.events[event_name] = [func]
            return func

        return inner

    async def dispatch(self, name: str, data: Dict[Any, Any]) -> None:
        """
        Dispatch a user event.

        Parameters
        ----------
        name: :class:`str`
            The event name to dispatch
        data: :class:`Dict[Any, Any]`
            The data to pass through to the event.
        """

        if name not in self.events:
            return

    async def start(
        self,
        token: str,
        *,
        session: ClientSession = None,
        loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """
        Starts the client.

        Parameters
        ----------
        token: :class:`str`
            The bot token to start the client with.
        session: :class:`ClientSession`
            The user-inputted session in case the user
            has a pre-defined session.
        """

        if not isinstance(token, str) or len(token) != 59:
            raise InvalidBotToken(
                "Make sure you enter a valid bot token instead of ``{}``".format(token)
            )

        self.loop = loop or asyncio.get_running_loop()
        session = session or ClientSession()
        self.http = HTTPClient(token=token, session=session, loop=self.loop)
        self.ws = await DiscordWebSocket.from_client(self)

        await self.ws.start()
