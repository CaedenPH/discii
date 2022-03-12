from __future__ import annotations

import asyncio
import json
import sys
import time

from aiohttp import ClientWebSocketResponse, WSMsgType, WSMessage
from typing import Any, Dict, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .client import Client

# fmt: off
__all__ = (
    'Route',
    'DiscordWebSocket',
)
# fmt: on


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
    _last_heartbeat: float

    def __init__(
        self,
        *,
        client: "Client",
        socket: ClientWebSocketResponse,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        self.client: Client = client
        self.socket: ClientWebSocketResponse = socket
        self.loop: asyncio.AbstractEventLoop = loop

        self.session_id: Optional[str] = None
        self.sequence: int = 0
        self.latency: float = 0

    @classmethod
    async def from_client(cls, client: "Client") -> DiscordWebSocket:
        http = client.http
        socket = await http.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")

        self = cls(client=client, socket=socket, loop=http.loop)
        self.token = http.token

        return self

    async def identify(self) -> None:
        """Sends the IDENTIFY payload through the websocket."""
        return await self.socket.send_json(
            {
                "op": self.IDENTIFY,
                "d": {
                    "token": self.token,
                    "intents": 513,
                    "properties": {
                        "$os": sys.platform,
                        "$browser": "my_library",
                        "$device": "my_library",
                    },
                },
            }
        )

    async def keep_alive(self) -> None:
        """
        Keeps the bot alive by
        sending a heartbeat every 30
        seconds.
        """
        while True:
            await self.socket.send_json({"op": self.HEARTBEAT, "d": self.sequence})
            self._last_heartbeat = time.perf_counter()
            await asyncio.sleep(self._heartbeat_interval)

    async def _parse_message(self, message_data: Dict[Any, Any]) -> None:
        """
        Parses the message data

        Parameters
        ----------
        message_data: :class:`Dict[Any, Any]`
            The raw message data passed through.
        """

        op = message_data["op"]
        data = message_data["d"]

        if op == self.HEARTBEAT_ACK:
            self.latency = time.perf_counter() - self._last_heartbeat
            return
        if op == self.DISPATCH and message_data["t"] == "GUILD_CREATE":
            return  # TODO: cache all guilds

        if op == self.DISPATCH and message_data["t"] == "READY":
            self.session_id = data["session_id"]

        if op == self.HELLO:
            await self.identify()
            self._heartbeat_interval = data["heartbeat_interval"] / 1000
            self.loop.create_task(self.keep_alive())

        if op == self.DISPATCH:
            self.sequence += 1
            await self.client.dispatch(message_data["t"], data)

        if not (op == self.DISPATCH and message_data["t"] == "GUILD_CREATE"):
            print(message_data)  # debugging

    async def listen(self) -> None:
        """
        Starts listening in to events being sent
        from the gateway. Sends IDENTIFY payload.
        """

        async for message in self.socket:  # type: WSMessage
            if message.type is WSMsgType.TEXT:
                await self._parse_message(json.loads(message.data))
            else:
                print(f"\n\n\n\n\n W H A T {message}")
                return
