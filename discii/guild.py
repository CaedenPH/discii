from typing import Dict, Any, List, Optional, Union

from .abc import Snowflake
from .channel import Channel, GuildCategory, TextChannel, VoiceChannel
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
        self.channels: List[Optional[Channel]] = [
            self._get_channel(payload=data) for data in payload["channels"]
        ]
        self.member_count = payload["member_count"]

    def _get_channel(self, payload: Dict[Any, Any]) -> Optional[Channel]:
        """
        Gets a channel object from the payload.

        Parameters
        ----------
        payload: :class:`Dict[Any, Any]`
            The payload to pass into the creating
            of the channel object.

        Returns
        -------
        the channel object created.
        """
        _channel_converter = {
            4: GuildCategory,
            2: VoiceChannel,
            0: TextChannel,
        }
        channel = _channel_converter.get(payload["type"])

        if channel is not None:
            return channel(payload=payload, state=self._state, guild=self)

    def get_channel(self, channel_id: int) -> Optional[Channel]:
        """
        Searches through the guilds channels
        to see whether or not the id matches
        ``channel_id``.

        Parameters
        ----------
        channel_id: :class:`int`
            The channel id to search for.
        """
        for channel in self.channels:
            if isinstance(channel, Channel):
                if channel.id == channel_id:
                    return channel

    async def ban(self, user_id: int) -> None:
        """
        Bans a user with an id of ``user_id``

        Parameters
        ----------
        user_id: :class:`int`
            The user id to ban.
        """
        await self._state.http.ban_user(guild_id=self.id, user_id=user_id)
