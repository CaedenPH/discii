from typing import Dict, Any, List, Optional

from .abc import Snowflake
from .channel import TextChannel
from .state import ClientState


# fmt: off
__all__ = (
    'Guild',
)
# fmt: on


class Guild(Snowflake):
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
        self._raw_payload = payload
        self._state = state
        self.id = int(payload["id"])
        self._channels: List[TextChannel] = [
            TextChannel(guild=self, payload=data, state=self._state)
            for data in payload["channels"]
        ]
        self.member_count = payload["member_count"]

    def get_channel(self, channel_id: int) -> Optional[TextChannel]:
        """
        Searches through the guilds channels
        to see whether or not the id matches
        ``channel_id``.

        Parameters
        ----------
        channel_id: :class:`int`
            The channel id to search for.
        """
        for channel in self._channels:
            if channel.id == channel_id:
                return channel
