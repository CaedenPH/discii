from typing import Any, Dict, TYPE_CHECKING

from .gateway import Route

if TYPE_CHECKING:
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

    async def delete(self) -> None:
        """
        Deletes the message
        """
        route = Route(
            "DELETE",
            "/channels/{channel_id}/messages/{message_id}".format(
                channel_id=self._raw_payload[
                    "channel_id"
                ],  # TODO: get from channel cache
                message_id=self.id,
            ),
        )
        await self._state.http.request(route)

    @property
    def id(self) -> int:
        """Returns the message id."""
        return self._id
