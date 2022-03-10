from enum import Enum
from typing import Any


class OPCODES(Enum):
    """Discord OP Codes"""

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class Route:
    BASE_URL: str = "https://discord.com/api/v10"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.path: str = path
        self.method: str = method
        self.url: str = self.BASE_URL + self.path
