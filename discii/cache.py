import collections
import weakref

from typing import Deque, List, Optional, TYPE_CHECKING

from .channel import TextChannel
from .guild import Guild
from .user import User

if TYPE_CHECKING:
    from .message import Message


# fmt: off
__all__ = (
    'Cache',
)
# fmt: on


class Cache:
    """
    The class that holds all the cached info.
    """

    def __init__(self) -> None:
        self.user: Optional[User] = None
        self._users: weakref.WeakValueDictionary[
            int, User
        ] = weakref.WeakValueDictionary()
        self._guilds: List[Guild] = []
        self._messages: Deque["Message"] = collections.deque()

    def add_guild(self, guild: Guild) -> None:
        self._guilds.append(guild)

    def add_message(self, message: "Message") -> None:
        self._messages.append(message)

    def get_message(self, message_id: int) -> Optional["Message"]:
        print(self._messages)

    def get_channel(self, channel_id: int) -> Optional[TextChannel]:
        for guild in self._guilds:
            channel = guild.get_channel(channel_id)
            if channel is not None:
                return channel
