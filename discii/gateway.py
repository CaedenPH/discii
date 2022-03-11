from __future__ import annotations

import asyncio
import sys
import aiohttp

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .http import HTTPClient

__all__ = (
    "Route",
    "DiscordWebSocket",
)


class Route:
    """
    Represents an api route which contains
    information about the call, including
    method and path.

    Parameters
    ----------
    method: :class:`str`
        The method to send to the api.
    path: :class:`str`
        The api path to send the data to.

    Attributes
    ----------
    BASE_URL: :class:`str`
        The base api url.
    """

    BASE_URL = "https://discord.com/api/v9"

    def __init__(self, method: str, path: str) -> None:
        self.method = method
        self.path = self.BASE_URL + path


class DiscordWebSocket:
    """
    Represents the connection between
    the discord gateway and the client.

    Attributes
    -----------
    DISPATCH
        Receive only. Denotes an event to be sent to Discord, such as READY.
    HEARTBEAT
        When received tells Discord to keep the connection alive.
        When sent asks if your connection is currently alive.
    IDENTIFY
        Send only. Starts a new session.
    PRESENCE
        Send only. Updates your presence.
    VOICE_STATE
        Send only. Starts a new connection to a voice guild.
    VOICE_PING
        Send only. Checks ping time to a voice guild, do not use.
    RESUME
        Send only. Resumes an existing connection.
    RECONNECT
        Receive only. Tells the client to reconnect to a new gateway.
    REQUEST_MEMBERS
        Send only. Asks for the full member list of a guild.
    INVALIDATE_SESSION
        Receive only. Tells the client to optionally invalidate the session
        and IDENTIFY again.
    HELLO
        Receive only. Tells the client the heartbeat interval.
    HEARTBEAT_ACK
        Receive only. Confirms receiving of a heartbeat. Not having it implies
        a connection issue.
    GUILD_SYNC
        Send only. Requests a guild sync.
    token
        The authentication token for the discord api.
    _heartbeat_interval
        The seconds to wait before sending another heartbeat.
    """

    # fmt: off
    DISPATCH           = 0 # noqa: ignore
    HEARTBEAT          = 1 # noqa: ignore
    IDENTIFY           = 2 # noqa: ignore
    PRESENCE           = 3 # noqa: ignore
    VOICE_STATE        = 4 # noqa: ignore
    VOICE_PING         = 5 # noqa: ignore
    RESUME             = 6 # noqa: ignore
    RECONNECT          = 7 # noqa: ignore
    REQUEST_MEMBERS    = 8 # noqa: ignore
    INVALIDATE_SESSION = 9 # noqa: ignore
    HELLO              = 10 # noqa: ignore
    HEARTBEAT_ACK      = 11 # noqa: ignore
    GUILD_SYNC         = 12 # noqa: ignore
    # fmt: on

    token: str
    _heartbeat_interval: float

    def __init__(self, *, socket: aiohttp.ClientWebSocketResponse, loop: asyncio.AbstractEventLoop) -> None:
        self.socket: aiohttp.ClientWebSocketResponse = socket
        self.loop: asyncio.AbstractEventLoop = loop

        self.session_id: Optional[str] = None
        self.sequence: Optional[float] = None

    @classmethod
    async def from_client(cls, http: HTTPClient) -> DiscordWebSocket:
        socket = await http.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        self = cls(socket=socket, loop=http.loop)
        return self

    async def identify(self) -> None:
        """Sends the IDENTIFY payload to the api."""
        return await self.socket.send_json(
            {
                "op": self.IDENTIFY,
                "d": {
                    "token": self.token,
                    "intents": 513,
                    "properties": {"$os": sys.platform, "$browser": "my_library", "$device": "my_library"},
                },
            }
        )
