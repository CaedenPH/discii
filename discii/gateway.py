from __future__ import annotations

import asyncio
import json
import sys
import time

from aiohttp import ClientWebSocketResponse, WSMsgType
from typing import Any, Dict, Optional, TYPE_CHECKING

from .guild import Guild
from .message import Message
from .user import User

if TYPE_CHECKING:
    from .cache import Cache
    from .client import Client
    from .state import ClientState

# fmt: off
__all__ = (
    'DiscordWebSocket',
)
# fmt: on


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
    DISPATCH           = 0
    HEARTBEAT          = 1
    IDENTIFY           = 2
    PRESENCE           = 3
    VOICE_STATE        = 4
    VOICE_PING         = 5
    RESUME             = 6
    RECONNECT          = 7
    REQUEST_MEMBERS    = 8
    INVALIDATE_SESSION = 9
    HELLO              = 10
    HEARTBEAT_ACK      = 11
    GUILD_SYNC         = 12
    # fmt: on

    token: str
    _heartbeat_interval: float
    _last_heartbeat: float
    _state: "ClientState"

    def __init__(
        self,
        *,
        client: "Client",
        socket: ClientWebSocketResponse,
        loop: asyncio.AbstractEventLoop,
        cache: "Cache",
    ) -> None:
        self.client: Client = client
        self.socket: ClientWebSocketResponse = socket
        self.loop: asyncio.AbstractEventLoop = loop
        self.cache: "Cache" = cache

        self.session_id: Optional[str] = None
        self.sequence: int = 0
        self.latency: float = 0

    @classmethod
    async def from_client(cls, client: "Client") -> DiscordWebSocket:
        http = client.http
        socket = await http.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")

        self = cls(client=client, socket=socket, loop=http.loop, cache=client._cache)
        self.token = http.token

        return self

    async def identify(self) -> None:
        """Sends the IDENTIFY payload through the websocket."""
        return await self.socket.send_json(
            {
                "op": self.IDENTIFY,
                "d": {
                    "token": self.token,
                    "intents": 32767,
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

    async def _request_guild_members(self, guild_id: int) -> None:
        return await self.socket.send_json(
            {
                "op": self.REQUEST_MEMBERS,
                "d": {"guild_id": guild_id, "query": "", "limit": 0},
            }
        )

    async def _cache_event(self, name: str, data: Dict[Any, Any]) -> None:
        if name == "GUILD_CREATE":
            guild = Guild(payload=data, state=self.state)
            self.cache.add_guild(guild)
            await self._request_guild_members(guild.id)

        elif name == "MESSAGE_CREATE":
            message = Message(payload=data, state=self.state)
            self.cache.add_message(message)

        elif name == "GUILD_MEMBERS_CHUNK":
            for _user in data["members"]:
                user = User(payload=_user["user"], state=self.state)
                self.cache.add_user(user)

    async def _parse_message(self, payload: Dict[Any, Any]) -> None:
        """
        Parses the message data

        Parameters
        ----------
        payload: :class:`Dict[Any, Any]`
            The raw message data passed through.
        """

        op = payload["op"]
        t = payload["t"]
        d = payload["d"]

        if op == self.HEARTBEAT_ACK:
            self.latency = time.perf_counter() - self._last_heartbeat
            return

        if op == self.DISPATCH and t == "READY":
            self.session_id = d["session_id"]

        if op == self.HELLO:
            await self.identify()
            self._heartbeat_interval = d["heartbeat_interval"] / 1000
            self.loop.create_task(self.keep_alive())

        if op == self.DISPATCH:
            self.sequence += 1
            await self.client.dispatch(t, d)

        await self._cache_event(t, d)

        return
        print(payload)  # debugging

    async def listen(self) -> None:
        """
        Starts listening in to events being sent
        from the gateway. Sends IDENTIFY payload.
        """

        self.state = self.client._get_state()
        async for message in self.socket:
            if message.type is WSMsgType.TEXT:
                await self._parse_message(json.loads(message.data))
            else:
                print(f"\n\n\n\n\n W H A T {message}")
                return
