from typing import TYPE_CHECKING

from .gateway import Route
from .state import ClientState

if TYPE_CHECKING:
    from .message import Message

__all__ = ("Channel", "DMChannel", "TextChannel")


class Channel:
    """
    Represents the base class
    which all discord channels
    inherit.
    """

    id: int

    def __init__(self, _state: ClientState) -> None:
        self._state = _state

    def _get_channel_id(self, id: int) -> int:
        raise NotImplementedError

    async def send(self, content: str) -> "Message":
        r = Route("POST", "/channels/{channel_id}/messages".format(channel_id=self._get_channel_id()))
        await self._state._http.request(r, json={})


class TextChannel(Channel):
    """
    Represents a discord channel
    """


class DMChannel(TextChannel):
    """
    Represents a direct message
    channel.
    """
