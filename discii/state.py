from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cache import Cache
    from .http import HTTPClient
    from .gateway import DiscordWebSocket


# fmt: off
__all__ = (
    'ClientState',
)
# fmt: on


class ClientState:
    """
    Represents a State with all the properties
    of `Client`.

    Parameters
    ----------
    http: :class:`HTTPClient`
        The http client which all requests
        are sent through.
    loop: :class:`asyncio.AbstractEventLoop`
        The loop that all tasks and events are
        ran off of.
    ws: :class:`DiscordWebSocket`
        The websocket connected to the gateway.
    cache: :class:`Cache`
        The cache which holds all the data sent
        and received from the gateway.
    """

    def __init__(self, *, http: "HTTPClient", ws: "DiscordWebSocket", cache: "Cache") -> None:
        self.http = http
        self.loop = http.loop
        self.ws = ws
        self.cache = cache
