import json
import aiohttp
import sys

from typing import Any, Dict
from aiohttp import ClientSession

from .gateway import Route
from . import __version__

__all__ = ("HTTPClient",)


class HTTPClient:
    """
    Used to make requests
    """

    def __init__(self, token: str, *, session: ClientSession) -> None:
        self.token = token
        self.session = session
        user_agent = "DiscordBot (https://github.com/CaedenPH/discii {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    async def request(self, route: Route, **kwargs: Any) -> Any:
        """make a request to the session"""

        headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
        }
        headers["Authorization"] = "Bot " + self.token
        kwargs["headers"] = headers

        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop("json"))

        async with self.session.request(route.method, route.url, **kwargs) as req:
            print(await req.json())
