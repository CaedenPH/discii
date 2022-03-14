from typing import Any, Dict


# fmt: off
__all__ = (
    'Embed',
)
# fmt: on


class Embed:
    """
    Represents a discord embed.

    Attributes
    ----------
    type: :class:`str`
        The embed type.
    """

    type: str = "rich"

    def __init__(
        self, *, title: str = None, description: str = None, colour: int = None
    ) -> None:
        self.title = title
        self.description = description
        self.colour = colour

    def _to_dict(self) -> Dict[str, Any]:
        _dict = {
            "title": self.title,
            "description": self.description,
            "color": self.colour,
        }
        return _dict
