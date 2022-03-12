from typing import Dict, Any

from .state import ClientState


# fmt: off
__all__ = (
    'Guild',
)
# fmt: on


class Guild:
    """
    Represents a discord guild.

    Parameters
    ----------
    payload: :class:`Dict[Any, Any]`
        The data received from the event.
    client_state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    """

    def __init__(self, *, payload: Dict[Any, Any], client_state: "ClientState") -> None:
        print(payload)
        self._raw_payload = payload
        self._client_state = client_state
