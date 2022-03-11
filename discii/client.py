import asyncio

from aiohttp import ClientSession


from .errors import InvalidBotToken
from .gateway import DiscordWebSocket
from .http import HTTPClient


__all__ = ("Client",)


class Client:
    """
    Represents a Client that interacts with
    the discord api and manages websocket connections.

    Attributes
    ----------
    loop: :class:`AbstractEventLoop`
        The loop to run all tasks and asynchronous
        coroutines run from.
    http: :class:`HTTPClient`
        The client which manages all interactions
        with the discord api.
    ws: :class:`DiscordWebSocket`
        The websocket to manage the gateway with
        the discord api.
    """

    def __init__(self) -> None:
        self.loop: asyncio.AbstractEventLoop
        self.http: HTTPClient
        self.ws: DiscordWebSocket

    async def start(
        self,
        token: str,
        *,
        session: ClientSession = None,
        loop: asyncio.AbstractEventLoop = None
    ) -> None:
        """
        Starts the client.

        Parameters
        ----------
        token: :class:`str`
            The bot token to start the client with.
        session: :class:`ClientSession`
            The user-inputted session in case the user
            has a pre-defined session.
        """

        if not isinstance(token, str) or len(token) != 59:
            raise InvalidBotToken(
                "Make sure you enter a valid bot token instead of ``{}``".format(token)
            )

        self.loop = loop or asyncio.get_running_loop()
        session = session or ClientSession()
        self.http = HTTPClient(token=token, session=session, loop=self.loop)
        self.ws = await DiscordWebSocket.from_client(self.http)

        await self.ws.start()
