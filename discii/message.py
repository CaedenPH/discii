from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ClientState

# fmt: off
__all__ = (
    'Message'
)
# fmt: on


class Message:
    """
    Represents a discord message.
    """

    def __init__(self, *, payload: Dict[Any, Any], client_state: "ClientState") -> None:
        self._raw_payload = payload
        self._client_state = client_state
