from typing import TYPE_CHECKING

if TYPE_CHECKING:
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
    ws: :class:`DiscordWebSocket`
        The websocket connected to the gateway.
    """

    def __init__(self, *, http: "HTTPClient", ws: "DiscordWebSocket") -> None:
        self.http = http
        self.loop = http.loop
        self.ws = ws
