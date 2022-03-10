from typing import Dict, Any

from .member import Member

class Message:
    """
    Represents a discord message.
    """

    def __init__(self, data: Dict[Any, Any]) -> None:
        print(data)
        self._raw_data = data
        self._content = data["content"]



    @property
    def content(self) -> str:
        """returns the message content or None"""
        return self._content or None

    @property
    def author(self) -> Member:
        """returns the author that sent the message"""