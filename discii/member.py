from typing import Any, Dict


__all__ = ("Member",)


class Member:
    """
    Represents a discord member.

    Parameters
    ----------
    data: :class:`Dict[Any, Any]`
        The raw payload received from
        the discord websocket.
    """

    def __init__(self, _data: Dict[Any, Any]) -> None:
        self._raw_data = _data
