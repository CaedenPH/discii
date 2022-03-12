import collections
import weakref

from typing import Deque, List, Optional

from .guild import Guild
from .message import Message
from .user import User

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
        self._guilds: List = []
        self._messages: Deque[Message] = collections.deque()

    def add_guild(self, guild: Guild) -> None:
        self._guilds.append(guild)

    def add_message(self, message: Message) -> None:
        self._messages.append(message)

    def get_message(self, message_id: int) -> None:
        print(self._messages)
