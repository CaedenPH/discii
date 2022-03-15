from typing import Any, Dict, TYPE_CHECKING, List

from .abc import Messageable, Snowflake

if TYPE_CHECKING:
    from .guild import Guild
    from .state import ClientState

# fmt: off
__all__ = (
    'ChannelType',
    'GuildCategory',
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


class GuildCategory(Snowflake):
    """
    Represents a discord category.

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    guild: :class:`Guild`
        The guild which the channel is in.
    """

    def __init__(self, *, payload: Dict[Any, Any], state: "ClientState", guild: "Guild"):
        self._raw_payload = payload
        self._state = state

        self.id = int(payload["id"])
        self.name: str = payload["name"]


class TextChannel(Messageable):
    """
    Represents a discord text channel

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    guild: :class:`Guild`
        The guild which the channel is in.

    Attributes
    ----------
    type: :class:`int`
        The channel type.
    """

    type: int = ChannelType.GUILD_TEXT

    def __init__(
        self,
        *,
        payload: Dict[Any, Any],
        state: "ClientState",
        guild: "Guild",
    ) -> None:
        self._raw_payload = payload
        self._state = state

        self.guild: "Guild" = guild

        self.id = int(payload["id"])
        self.position: int = int(payload["position"])
        self.slowmode: int = payload["rate_limit_per_user"]

        self.name: str = payload["name"]
        self.topic: str = payload["topic"]

    async def _get_channel_id(self) -> int:
        return self.id

class VoiceChannel(Snowflake):
    """
    Represents a discord text channel

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    guild: :class:`Guild`
        The guild which the channel is in.

    Attributes
    ----------
    type: :class:`int`
        The channel type.
    """
    type: int = ChannelType.GUILD_VOICE

    def __init__(
        self,
        *,
        payload: Dict[Any, Any],
        state: "ClientState",
        guild: "Guild",
    ) -> None:
        self._raw_payload = payload
        self._state = state

        self.id = int(payload["id"])
        self.name: str = payload["name"]


class DMChannel(TextChannel):
    """
    Represents a discord dm channel.

    Attributes
    ----------
    type: :class:`int`
        The channel type.
    """
    type: int = ChannelType.DM
