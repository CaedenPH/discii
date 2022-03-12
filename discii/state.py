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
    def __init__(self, *, http: "HTTPClient", ws: "DiscordWebSocket") -> None:
        self.http = http
        self.loop = http.loop
        self.ws = ws
