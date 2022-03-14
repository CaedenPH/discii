import collections
import weakref

from typing import Deque, List, Optional, TYPE_CHECKING

from .channel import TextChannel
from .errors import ChannelNotFound
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
    The class that holds all the cached data.

    Attributes
    ----------
    user: :class:`Optional[User]`
        The client user in User object. Injected
        into cache after the `READY` event has
        been received.
    _users: :class:`weakref.WeakValueDictionary[int, User]`
        A dictionary of all users where the
        key is the user id. Can be easily
        conerted to a Member object.
    _guilds: :class:`List[Guild]`
        The list of guilds that the bot is in.
    _messages: :class:`Deque["Message"]`
        A `collections.deque` of message objects
        to optimize speed-time access.
    """

    def __init__(self) -> None:
        self.user: Optional[User] = None
        self._users: weakref.WeakValueDictionary[
            int, User
        ] = weakref.WeakValueDictionary()
        self._guilds: List[Guild] = []
        self._messages: Deque["Message"] = collections.deque()

    def add_guild(self, guild: Guild) -> None:
        """
        Adds a guild to the internal guild cache.

        Parameters
        ----------
        guild: :class:`Guild`
            The guild to add to the cache.
        """
        self._guilds.append(guild)

    def add_message(self, message: "Message") -> None:
        """
        Adds a message to the internal guild cache.

        Parameters
        ----------
        message: :class:`Message`
            The message to add to the cache.
        """
        self._messages.append(message)

    def get_message(self, message_id: int) -> Optional["Message"]:
        """
        Searches the internal cache for a message

        Parameters
        ----------
        message_id: :class:`int`
            The message id to find.

        Returns
        -------
        message: :class:`Message`
            The message if found, else `None`
        """
        message = [message for message in self._messages if message.id == message_id]
        if message is not None:
            return message[0]
        return None

    def get_guild(self, guild_id: int) -> Optional[Guild]:
        """
        Searches the internal cache for a guild.

        Parameters
        ----------
        guild_id: :class:`int`
            The guild's id.

        Returns
        -------
        guild: :class:`Guild`
            The guild if found, else None
        """
        guild = [guild for guild in self._guilds if guild.id == guild_id]
        if guild is not None:
            return guild[0]
        return None

    def get_channel(self, channel_id: int) -> TextChannel:
        """
        Searches the internal cache for a channel.

        Parameters
        ----------
        channel_id: :class:`int`
            The channel id to find.

        Returns
        -------
        channel: :class:`TextChannel`
            The channel if found, else `None`
        """
        for guild in self._guilds:
            channel = guild.get_channel(channel_id)
            if channel is not None:
                return channel
        raise ChannelNotFound("Channel with id ``{}`` not found".format(channel_id))
