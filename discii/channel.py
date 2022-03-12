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
    client_state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    """

    def __init__(self, *, payload: Dict[Any, Any], client_state: "ClientState") -> None:
        self._raw_payload = payload
        self._client_state = client_state


class TextChannel(Channel):
    """
    Represents a discord text channel
    """


class DMChannel(TextChannel):
    """
    Represents a discord dm channel.
    """
