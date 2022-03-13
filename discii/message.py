from typing import Any, Dict, TYPE_CHECKING

from .http import Route
from .user import Member

if TYPE_CHECKING:
    from .channel import TextChannel
    from .state import ClientState

# fmt: off
__all__ = (
    'Message',
)
# fmt: on


class Message:
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
        self._id = payload["id"]
        self._content = payload["content"]
        self._channel = self._state.cache.get_channel(payload["channel_id"])
        self._author = Member(payload=payload["author"], state=self._state)

    async def delete(self) -> None:
        """
        Deletes the message
        """
        route = Route(
            "DELETE",
            "/channels/{channel_id}/messages/{message_id}".format(
                channel_id=self.channel.id,
                message_id=self.id,
            ),
        )
        await self._state.http.request(route)

    @property
    def id(self) -> int:
        """Returns the message id."""
        return self._id

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
