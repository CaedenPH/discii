from __future__ import annotations

from typing import Any, Dict, TYPE_CHECKING

from .abc import Snowflake
from .user import Member

if TYPE_CHECKING:
    from .channel import TextChannel
    from .state import ClientState

# fmt: off
__all__ = (
    'Message',
)
# fmt: on


class Message(Snowflake):
    """
    Represents a discord message.

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    _state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    """

    def __init__(self, *, payload: Dict[Any, Any], state: "ClientState") -> None:
        self._raw_payload = payload
        self._state = state
        self.id = payload["id"]
        self._content = payload["content"]
        self._channel = self._state.cache.get_channel(payload["channel_id"])
        self._author = Member(payload=payload["author"], state=self._state)

    async def delete(self) -> None:
        """
        Deletes the message
        """
        await self._state.http.delete_message(
            message_id=self.id, channel_id=self.channel.id
        )

    async def reply(self, content: str) -> Message:
        """
        Replies to the message.

        Parameters
        ----------
        content: :class:`str`
            The content to send."""
        return await self._state.http.send_message(
            self.channel.id,
            content=content,
            message_reference={"message_id": self.id, "guild_id": self.channel.guild.id},
        )

    @property
    def channel(self) -> "TextChannel":
        """Returns the channel that the message was sent in."""
        return self._channel  # type: ignore

    @property
    def content(self) -> str:
        """Returns the message content."""
        return self._content

    @property
    def author(self) -> Member:
        """Returns the author who sent the message."""
        return self._author
