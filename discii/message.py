from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, TYPE_CHECKING, List

from .abc import Snowflake
from .embed import Embed
from .user import Member

if TYPE_CHECKING:
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

        self.id = int(payload["id"])
        self.timestamp = datetime.fromisoformat(payload["timestamp"])
        self.content: str = payload["content"]
        self.channel = self._state.cache.get_channel(int(payload["channel_id"]))
        self.guild = self.channel.guild
        self.author = Member(payload=payload["author"], state=self._state)

    async def delete(self) -> None:
        """
        Deletes the message.
        """
        await self._state.http.delete_message(
            message_id=self.id, channel_id=self.channel.id
        )

    async def edit(self, content: str = None, *, embeds: List[Embed] = None) -> Message:
        """
        Edits the message.

        Parameters
        ----------
        content: :class:`str`
            The content to edit to.
        embeds: :class:`List[Embed]`
            The embeds to add to the message.
        """
        return await self._state.http.edit_message(
            self.channel.id,
            message_id=self.id,
            content=content,
            embeds=embeds,
        )
    
    async def reply(self, content: str = None, *, embeds: List[Embed] = None) -> Message:
        """
        Replies to the message.

        Parameters
        ----------
        content: :class:`str`
            The content to send.
        embeds: :class:`List[Embed]`
            The message embeds.
        """
        return await self._state.http.send_message(
            self.channel.id,
            content=content,
            embeds=embeds,
            message_reference={
                "message_id": self.id,
                "guild_id": getattr(self.guild, "id", None),
            },
        )
