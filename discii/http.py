from asyncio import AbstractEventLoop
from aiohttp import ClientSession, ClientWebSocketResponse


__all__ = ("HTTPClient",)


class HTTPClient:
    """
    Represents the client that manages
    interactions to the discord api.

    Parameters
    ----------
    token: :class:`str`
        The bot token to pass through the
        authorization headers while interacting
        with the discord api.
    session: :class:`ClientSession`
        The session to make requests from
        and to handle interactions with the api.
    """

    def __init__(self, *, token: str, loop: AbstractEventLoop, session: ClientSession) -> None:
        self.token = token
        self.loop = loop
        self._session = session

    async def ws_connect(self, gateway_url: str) -> ClientWebSocketResponse:
        """
        Connects to the gateway.

        Parameters
        ----------
        gateway_url: :class:`str`
            The gateway url to connect to.
        """
        return await self._session.ws_connect(gateway_url)
