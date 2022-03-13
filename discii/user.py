from typing import Any, Dict, TYPE_CHECKING

from .abc import Snowflake

if TYPE_CHECKING:
    from .state import ClientState

# fmt: off
__all__ = (
    'User',
    'Member',
)
# fmt: on


class User(Snowflake):
    """
    Represents a discord user

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
        self._bot: bool = payload.get("bot", False)

    @property
    def bot(self) -> bool:
        """Returns whether or not the author is a bot."""
        return self._bot


class Member(User):
    """
    Represents a guild-bound discord member.
    """
