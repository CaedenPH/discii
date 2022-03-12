from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ClientState

# fmt: off
__all__ = (
    'Channel',
    'TextChannel',
    'DMChannel',
)
# fmt: on


class Channel:
    """
    The base class for all channels.

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    _state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    """

    def __init__(self, *, payload: Dict[Any, Any], state: "ClientState") -> None:
        # TODO: parse
        self._raw_payload = payload
        self._state = state
        self._id = payload["id"]
        self._name = payload["name"]

    @property
    def id(self) -> int:
        """Returns the channel id"""
        return self._id

    @property
    def name(self) -> str:
        """Returns the channel name"""
        return self._name


class TextChannel(Channel):
    """
    Represents a discord text channel
    """


class DMChannel(TextChannel):
    """
    Represents a discord dm channel.
    """
