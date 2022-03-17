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
    title: :class:`str`
        The embed title.
    description: :class:`str`
        The embed description.
    colour: :class:`int`
        The embed colour in hex format.
    timestamp: :class:`datetime`
        The ISO8601 timestamp.
    thumbnail: :class:`Optional[Dict[str, str]]`
        The embed thumbnail.
    video: :class:`Optional[Dict[str, str]]`
        The embed video.
    image: :class:`Optional[Dict[str, str]]`
        The embed image.
    author: :class:`Optional[Dict[str, Optional[str]]]`
        The embed author.
    footer: :class:`Optional[Dict[str, Optional[str]]]`
        The embed footer.
    fields: :class:`List[Dict[str, Union[str, bool]]]`
        A list of the embeds fields.
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
        """
        Sets the thumnail field.

        Parameters
        ----------
        url: :class:`str`
            The thumbnail url.
        """
        self.thumbnail = {"url": url}

    def set_video(self, url: str) -> None:
        """
        Sets the video field.

        Parameters
        ----------
        url: :class:`str`
            The video url.
        """
        self.video = {"url": url}

    def set_image(self, url: str) -> None:
        """
        Sets the image field.

        Parameters
        ----------
        url: :class:`str`
            The image url.
        """
        self.image = {"url": url}

    def set_author(self, name: str, icon_url: str = None) -> None:
        """
        Sets the author field.

        Parameters
        ----------
        name: :class:`str`
            The author name.
        icon_url: :class:`str`
            The author icon_url.
        """
        self.author = {"name": name, "icon_url": icon_url}

    def set_footer(self, text: str, icon_url: str = None) -> None:
        """
        Sets the footer field.

        Parameters
        ----------
        text: :class:`str`
            The footer text.
        icon_url: :class:`str`
            The footer icon_url.
        """
        self.footer = {"text": text, "icon_url": icon_url}

    def add_field(
        self, name: str = NO_WIDTH_CHAR, value: str = NO_WIDTH_CHAR, inline: bool = False
    ) -> None:
        """
        Adds a field to the embed.

        Parameters
        ----------
        name: :class:`str`
            The field name. Defaults to
            an ascii no width char.
        value: :class:`str`
            The field value. Defaults to
            an ascii no width char.
        """
        self.fields.append({"name": name, "value": value, "inline": inline})

    def _to_dict(self) -> Dict[str, Any]:
        """
        Converts the current state to a json-
        parsiable dictionary.

        Returns
        -------
        _dict: :class:`Dict[str, Any]`
            The json-parsonable dict representing
            the current embed state.
        """
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
