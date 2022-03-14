from typing import Any, Dict, List, Optional, Union
from datetime import datetime


# fmt: off
__all__ = (
    'Embed',
)
# fmt: on

NO_WIDTH_CHAR = "\u200b"


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
        self,
        *,
        title: str = None,
        description: str = None,
        colour: int = None,
        timestamp: datetime = None,
    ) -> None:
        self.title = title
        self.description = description
        self.colour = colour
        self.timestamp = timestamp

        self.thumbnail: Optional[Dict[str, str]] = None
        self.video: Optional[Dict[str, str]] = None
        self.image: Optional[Dict[str, str]] = None
        self.author: Optional[Dict[str, Optional[str]]] = None
        self.footer: Optional[Dict[str, Optional[str]]] = None
        self.fields: List[Dict[str, Union[str, bool]]] = []

    def set_thumbnail(self, url: str) -> None:
        self.thumbnail = {
            "url": url,
        }

    def set_video(self, url: str) -> None:
        self.video = {"url": url}

    def set_image(self, url: str) -> None:
        self.image = {"url": url}

    def set_author(self, name: str, icon_url: str = None) -> None:
        """
        Sets the author field.

        Parameters
        ----------
        name: :class:`str`
            The author name.
        icon_url: :class:`str`
            The icon url to assign.
        """
        self.author = {"name": name, "icon_url": icon_url}

    def set_footer(self, text: str, icon_url: str = None) -> None:
        self.footer = {"text": text, "icon_url": icon_url}

    def add_field(
        self, name: str = NO_WIDTH_CHAR, value: str = NO_WIDTH_CHAR, inline: bool = False
    ) -> None:
        self.fields.append({"name": name, "value": value, "inline": inline})

    def _to_dict(self) -> Dict[str, Any]:
        _dict = {
            "title": self.title,
            "description": self.description,
            "color": self.colour,
            "thumbnail": self.thumbnail,
            "video": self.video,
            "image": self.image,
            "author": self.author,
            "footer": self.footer,
            "fields": self.fields,
        }
        if self.timestamp is not None:
            _dict["timestamp"] = self.timestamp.isoformat()
        return _dict
