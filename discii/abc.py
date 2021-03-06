from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .embed import Embed
    from .message import Message
    from .guild import Guild
    from .state import ClientState

# fmt: off
__all__ = (
    'Snowflake',
    'Messageable',
)
# fmt: on


class Snowflake:
    """
    The abstract snowflake which all models
    and objects will inherit from.

    Attributes
    ----------
    id: :class:`int`
        The id that the snowflake has.
    """

    id: int


class Messageable(Snowflake):
    """
    Represents a channel in which messages
    can be sent and received, for example a
    guild text channel or a user dm channel.

    Attributes
    ----------
    _state: :class:`ClientState`
        The client's state used to make requests.
    """

    _state: "ClientState"

    async def _get_channel_id(self) -> int:
        raise NotImplementedError

    async def send(self, text: str = None, *, embeds: List["Embed"] = None) -> "Message":
        """
        Sends a message to the channel.

        Parameters
        ----------
        text: :class:`str`
            The text to send to the channel.
        embeds: :class:`List[Embed]`
            The message embeds.
        """
        channel_id = await self._get_channel_id()
        return await self._state.http.send_message(channel_id, text=text, embeds=embeds)


class Repliable(Snowflake):
    """
    Represents a message that can be
    replied to.

    Attributes
    ----------
    _state: :class:`ClientState`
        The client's state used to make requests.
    """

    _state: "ClientState"
    message: "Message"
    guild: "Guild"

    async def reply(self, text: str = None, *, embeds: List["Embed"] = None) -> "Message":
        """
        Replies to the message.

        Parameters
        ----------
        text: :class:`str`
            The text to send.
        embeds: :class:`List[Embed]`
            The message embeds.
        """
        return await self._state.http.send_message(
            self.message.id,
            text=text,
            embeds=embeds,
            message_reference={
                "message_id": self.id,
                "guild_id": getattr(self.guild, "id", None),
            },
        )
