import asyncio
import sys
import traceback

from aiohttp import ClientSession
from typing import Any, Dict, List, Optional, TypeVar, Callable, Coroutine, TYPE_CHECKING


from .cache import Cache
from .converters import _event_to_object
from .errors import ChannelNotFound, InvalidBotToken, InvalidFunction, UserNotFound
from .gateway import DiscordWebSocket
from .http import HTTPClient
from .state import ClientState

if TYPE_CHECKING:
    from .channel import Channel
    from .guild import Guild
    from .message import Message
    from .user import User


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

        self._cache = Cache()
        self.events: Dict[str, List[Callable[..., Coroutine[Any, Any, Any]]]] = {}
        self.error_handlers: Dict[str, Callable[..., Coroutine[Any, Any, Any]]] = {}

    @property
    def latency(self) -> float:
        """Returns the clients latency."""
        return self.ws.latency

    @property
    def user(self) -> Optional["User"]:
        """Returns the user the client is logged
        in as. If its not logged in it will return None."""
        return self._cache.user

    def _get_state(self) -> ClientState:
        return ClientState(http=self.http, ws=self.ws, cache=self._cache)

    def _parse_event_data(self, name: str, data: Dict[Any, Any]) -> Any:
        """
        Parses an event with it's data

        Parameters
        ----------
        name: :class:`str`
            The event name to parse.
        data: :class:`Dict[Any, Any]`
            The data to parse.

        Returns
        -------
        data: :class:`Any`
            The pretty data to pass into the
            coro itself.
        """

        state = self._get_state()
        state = _event_to_object(name, data, state)
        if state is None:
            return ()
        return state

    async def _run_event(
        self, coro: Callable[..., Coroutine[Any, Any, Any]], *args, **kwargs
    ) -> None:
        """
        Runs the event in a localised task.

        Parameters
        ----------
        coro: :class:`Coro`
            The coroutine to run.
        """
        try:
            await coro(*args, **kwargs)
        except Exception as error:
            await self.on_error(error, coro)

    async def on_error(
        self, error: Any, coro: Callable[..., Coroutine[Any, Any, Any]]
    ) -> None:
        if coro.__name__ in self.error_handlers:
            handler = self.error_handlers[coro.__name__]
            return await handler(error)
        if "global" in self.error_handlers:
            handler = self.error_handlers["global"]
            return await handler(error, coro)

        print(f"Exception in {coro.__name__}", file=sys.stderr)
        traceback.print_exc()

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

        for coro in self.events[name]:
            args = (
                self._parse_event_data(name, data)
                if not getattr(coro, "__raw", False)
                else data
            )
            self.loop.create_task(self._run_event(coro, *args))

    async def start(
        self,
        token: str,
        *,
        session: ClientSession = None,
        loop: asyncio.AbstractEventLoop = None,
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
        loop: :class:`AbstractEventLoop`
            The loop to to use in case the user has an
            event loop.
        """

        if not isinstance(token, str) or len(token) != 59:
            raise InvalidBotToken(
                "Make sure you enter a valid bot token instead of ``{}``".format(token)
            )

        self.loop = loop or asyncio.get_running_loop()
        session = session or ClientSession()
        self.http = HTTPClient(token=token, session=session, loop=self.loop, client=self)
        self.ws = await DiscordWebSocket.from_client(self)

        await self.ws.listen()  # blocking to keep code running.

    def error(self, coro: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        """
        Decorator to register a global event
        handler.

        Parameters
        ----------
        coro: :class:`Coro`
            The coroutine to register as the error handler.
        """
        self.error_handlers["global"] = coro

    def on(self, event_name: str, *, raw: bool = False) -> Any:
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

        def inner(coro: Coro) -> Coro:
            if not asyncio.iscoroutinefunction(coro):
                raise InvalidFunction("Your event must be a coroutine.")

            coro.__raw = raw
            if event_name in self.events:
                self.events[event_name].append(coro)
            else:
                self.events[event_name] = [coro]
            return coro

        return inner

    def get_channel(self, channel_id: int) -> Optional["Channel"]:
        """
        Attempts to get a channel with an id
        of ``channel_id``.

        Parameters
        ----------
        channel_id: :class:`int`
            The channel's id.

        Returns
        -------
        channel: :class:`TextChannel`
            The channel if found, else None
        """
        try:
            return self._cache.get_channel(channel_id)
        except ChannelNotFound:
            return None

    def get_message(self, message_id: int) -> Optional["Message"]:
        """
        Attempts to get a message with an id
        of ``message_id``.

        Parameters
        ----------
        message_id: :class:`int`
            The message's id.

        Returns
        -------
        message: :class:`Message`
            The message if found, else None
        """
        return self._cache.get_message(message_id)

    def get_guild(self, guild_id: int) -> Optional["Guild"]:
        """
        Attempts to get a guild with an id
        of ``guild_id``.

        Parameters
        ----------
        guild_id: :class:`int`
            The guild's id.

        Returns
        -------
        guild: :class:`Guild`
            The guild if found, else None
        """
        return self._cache.get_guild(guild_id)

    def get_user(self, user_id: int) -> Optional["User"]:
        """
        Attempts to get a user with an id
        of ``user_id``.

        Parameters
        ----------
        user_id: :class:`int`
            The user's id.

        Returns
        -------
        user: :class:`User`
            The user if found, else None
        """
        try:
            return self._cache.get_user(user_id)
        except UserNotFound:
            return None
