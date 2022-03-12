from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ClientState

# fmt: off
__all__ = (
    'User',
    'Member',
)
# fmt: on


class User:
    """
    Represents a discord user

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


class Member:
    """
    Represents a guild-bound discord member.
    """
