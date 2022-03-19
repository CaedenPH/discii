from typing import Any, Dict, TYPE_CHECKING

from .abc import Messageable

if TYPE_CHECKING:
    from .state import ClientState


# fmt: off
__all__ = (
    'User',
    'Member',
)
# fmt: on


class User(Messageable):
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

        self.id = int(payload["id"])
        self.bot: bool = payload.get("bot", False)

    async def _get_channel_id(self) -> int:
        channel_id = await self._state.http.create_dm(self.id)
        return channel_id


class Member(User):
    """
    Represents a guild-bound discord member.
    """
