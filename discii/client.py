__all__ = ("Client",)


class Client:
    """
    Represents a Client that interacts with
    the discord api and manages websocket connections.
    """

    def __init__(self) -> None:
        """"""

    async def start(self, token: str) -> None:
        """
        Starts the client.

        Parameters
        ----------
        token: :class:`str`
            The bot token to start the client with.
        """
