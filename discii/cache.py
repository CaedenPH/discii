import collections

from typing import Dict, Deque, List, Optional, Union, TYPE_CHECKING

from .channel import TextChannel, DMChannel, GuildCategory, VoiceChannel
from .errors import ChannelNotFound, UserNotFound
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
        self._users: Dict[int, User] = {}
        self._guilds: List[Guild] = []
        self._dm_channels: List[DMChannel] = []
        self._messages: Deque["Message"] = collections.deque()

    def set_bot_user(self, user: User) -> None:
        """
        Sets the bot user.

        Parameters
        ----------
        users: :class:`User`
            The client user.
        """
        self.user = user

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

    def add_user(self, user: User) -> None:

        """
        Adds a user to the internal guild cache.

        Parameters
        ----------
        user: :class:`User`
            The guild to add to the cache.
        """
        self._users[user.id] = user

    def add_dm_channel(self, channel: DMChannel) -> None:
        """
        Adds a dm channel to the internal guild cache.

        Parameters
        ----------
        channel: :class:`DMChannel`
            The dm channel to add to the cache.
        """
        self._dm_channels.append(channel)

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
        message = list(filter(lambda m: m.id == message_id, self._messages))
        return message[0] if message else None

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
        guild = list(filter(lambda g: g.id == guild_id, self._guilds))
        return guild[0] if guild else None

    def get_channel(
        self, channel_id: int
    ) -> Union[TextChannel, DMChannel, GuildCategory, VoiceChannel]:
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

        dm_channel = list(filter(lambda d: d.id == channel_id, self._dm_channels))
        if dm_channel:
            return dm_channel[0]
        raise ChannelNotFound("Channel with id ``{}`` not found".format(channel_id))

    def get_user(self, user_id: int) -> User:
        """
        Searches the internal cache for a user.

        Parameters
        ----------
        user_id: :class:`int`
            The user id to find.

        Returns
        -------
        user: :class:`User`
            The user if found, else `None`
        """
        if user_id in self._users:
            return self._users[user_id]
        raise UserNotFound("User with id ``{}`` not found".format(user_id))
