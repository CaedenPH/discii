from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .embed import Embed
    from .message import Message
    from .state import ClientState

# fmt: off
__all__ = (
    "Snowflake",
    "Messageable",
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

    async def send(
        self, content: str = None, *, embeds: List["Embed"] = None
    ) -> "Message":
        """
        Sends a message to the channel.

        Parameters
        ----------
        content: :class:`str`
            The content to send to the channel.
        """
        channel_id = await self._get_channel_id()
        return await self._state.http.send_message(
            channel_id,
            content=content,
            embeds=embeds,
        )
