import pprint

from typing import Dict, Any, List, Optional

from .channel import TextChannel
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
    _state: :class:`ClientState`
        The client state which holds the
        necessary attributes to perform actions.
    """

    def __init__(self, *, payload: Dict[Any, Any], state: "ClientState") -> None:
        pprint.pprint(payload)
        self._raw_payload = payload
        self._state = state
        self._channels: List[TextChannel] = [
            TextChannel(payload=data, state=self._state) for data in payload["channels"]
        ]

        self.member_count = payload["member_count"]

    def get_channel(self, channel_id: int) -> Optional[TextChannel]:
        for channel in self._channels:
            if channel.id == channel_id:
                return channel
