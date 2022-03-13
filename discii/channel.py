from typing import Any, Dict, TYPE_CHECKING

from .abc import Snowflake
from .message import Message

if TYPE_CHECKING:
    from .guild import Guild
    from .state import ClientState

# fmt: off
__all__ = (
    'ChannelType',
    'TextChannel',
    'DMChannel',
)
# fmt: on


class ChannelType:
    """
    Represents the channel types.

    Attributes
    ----------
    GUILD_TEXT
        a text channel within a server
    DM
        a direct message between users
    GUILD_VOICE
        a voice channel within a server
    GROUP_DM
        a direct message between multiple users
    GUILD_CATEGORY
        an organizational category that contains up to 50 channels
    GUILD_NEWS
        a channel that users can follow and crosspost into their own server
    GUILD_STORE
        a channel in which game developers can sell their game on Discord
    GUILD_NEWS_THREAD
        a temporary sub-channel within a GUILD_NEWS channel
    GUILD_PUBLIC_THREAD
        a temporary sub-channel within a GUILD_TEXT channel
    GUILD_PRIVATE_THREAD
        a temporary sub-channel within a GUILD_TEXT channel that is
        only viewable by those invited and those with the MANAGE_THREADS permission
    GUILD_STAGE_VOICE
        a voice channel for hosting events with an audience
    """

    # fmt: off
    GUILD_TEXT =           0 # noqa: ignore
    DM =                   1 # noqa: ignore
    GUILD_VOICE =          2 # noqa: ignore
    GROUP_DM =             3 # noqa: ignore
    GUILD_CATEGORY =       4 # noqa: ignore
    GUILD_NEWS =           5 # noqa: ignore
    GUILD_STORE =          6 # noqa: ignore
    GUILD_NEWS_THREAD =    10 # noqa: ignore
    GUILD_PUBLIC_THREAD =  11 # noqa: ignore
    GUILD_PRIVATE_THREAD = 12 # noqa: ignore
    GUILD_STAGE_VOICE =    13 # noqa: ignore
    # fmt: on


class TextChannel(Snowflake):
    """
    Represents a discord text channel

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    _state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.

    Attributes
    ----------
    _type: :class:`int`
        The channel type.
    """

    _type: int = ChannelType.GUILD_TEXT

    def __init__(
        self, *, guild: "Guild", payload: Dict[Any, Any], state: "ClientState"
    ) -> None:
        # TODO: parse
        self._raw_payload = payload
        self._state = state
        self.id = payload["id"]
        self._name = payload["name"]
        self._guild = guild

    @property
    def name(self) -> str:
        """Returns the channel name"""
        return self._name

    @property
    def guild(self) -> "Guild":
        """Returns the guild the channel is in."""
        return self._guild

    async def send(self, content: str) -> Message:
        """
        Sends a message to the channel.

        Parameters
        ----------
        content: :class:`str`
            The content to send to the channel.

        .. more params to add.
        """
        return await self._state.http.send_message(self.id, content=content)


class DMChannel(TextChannel):
    """
    Represents a discord dm channel.

    Attributes
    ----------
    _type: :class:`int`
        The channel type.
    """

    _type: int = ChannelType.DM
