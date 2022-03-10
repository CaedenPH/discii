from typing import Union, Dict, Any

from .channel import TextChannel, DMChannel
from .member import Member
from .state import ClientState


__all__ = ("Message",)


class Message:
    """
    Represents a discord message.

    Parameters
    ----------
    data: :class:`Dict[Any, Any]`
        The raw payload received from
        the discord websocket.
    """

    def __init__(
        self,
        _state: ClientState,
        _data: Dict[Any, Any],
    ) -> None:
        print(_data)
        self._raw_data = _data
        self._state = _state
        self._content = _data["content"]
        self._author = Member(_data["member"])

    @property
    def content(self) -> str:
        """returns the message content or None"""
        return self._content or None

    @property
    def author(self) -> Member:
        """returns the author that sent the message"""
        return self._author

    @property
    def channel(self) -> Union[TextChannel, DMChannel]:
        """returns the channel that the message was sent in."""
        return self._channel
