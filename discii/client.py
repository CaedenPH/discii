from .errors import InvalidBotToken


__all__ = ("Client",)


class Client:
    """
    Represents a Client that interacts with
    the discord api and manages websocket connections.
    """

    async def start(self, token: str) -> None:
        """
        Starts the client.

        Parameters
        ----------
        token: :class:`str`
            The bot token to start the client with.
        """

        if not isinstance(token, str) or len(token) != 59:
            raise InvalidBotToken("Make sure you enter a valid bot token instead of ``{}``".format(token))

    