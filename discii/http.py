import json
import sys
import aiohttp

from asyncio import AbstractEventLoop
from aiohttp import ClientSession, ClientWebSocketResponse
from typing import Dict, Any

from . import __version__
from .gateway import Route

# fmt: off
__all__ = (
    'HTTPClient',
)
# fmt: on


class HTTPClient:
    """
    Represents the HTTP client that manages
    interactions to the discord api which
    entails sending custom requests with bot
    specific authorization headers.

    Parameters
    ----------
    token: :class:`str`
        The bot token to pass through the
        authorization headers while interacting
        with the discord api.
    loop: :class:`AbstractEventLoop`
        The event loop that all tasks run from.
    _session: :class:`ClientSession`
        The session to make requests from
        and to handle interactions with the api.
    user_agent: :class:`str`
        The user agent to pass through authorization
        so that the discord api is less suspicious.
    """

    def __init__(
        self, *, token: str, loop: AbstractEventLoop, session: ClientSession
    ) -> None:
        self.token = token
        self.loop = loop
        self._session = session

        user_agent = "DiscordBot (https://github.com/CaedenPH/discii {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )

    async def ws_connect(self, gateway_url: str) -> ClientWebSocketResponse:
        """
        Connects to the gateway.

        Parameters
        ----------
        gateway_url: :class:`str`
            The gateway url to connect to.
        """
        return await self._session.ws_connect(gateway_url)

    async def request(self, route: Route, **kwargs: Any) -> Any:
        """
        Sends a request through the session

        Parameters
        ----------
        route: :class:`Route`
            The route class which contains the
            method and path of the request.
        kwargs: :class:`Dict[Any, Any]`
            The dict containing the information
            to be passed into the request. If found,
            the json param will be auto-converted to
            the headers passed.
        """

        headers: Dict = {"User-Agent": self.user_agent}
        headers["Authorization"] = "Bot " + self.token

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.loads(kwargs.pop("json"))

        kwargs["headers"] = headers

        async with self._session.request(route.method, route.path, **kwargs) as req:
            return req
