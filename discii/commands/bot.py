import discii

from typing import TypeVar, Union, Optional, List, Dict, Coroutine, Callable, Any

from .core import Command, Context


# fmt: off
__all__ = (
    'Bot',
)
# fmt: on


Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


class Bot(discii.Client):
    """
    A bot that handles commands and slash
    command interactions.

    Attributes
    ----------
    prefix: :class:`List[str]`
        The prefix that the bot listens to
        to check for commands.
    """

    def __init__(self, *, prefixes: List[str]) -> None:
        super().__init__()

        self.events: Dict[str, List[Callable[..., Coroutine[Any, Any, Any]]]] = {
            "MESSAGE_CREATE": [self._message_create]
        }
        self.prefixes: List[str] = prefixes
        self._all_commands: Dict[str, Command] = {}

    def command(self, names: List[str]) -> Any:
        """ """

        def inner(coro: Coro) -> Coro:
            command = Command(coro, names=names)

            for name in names:
                self._all_commands[name] = command

            return coro

        return inner

    def _get_command(self, text: str) -> Optional[Command]:
        for prefix in self.prefixes:
            if text.startswith(prefix):
                break
        else:
            return None

        command = text[len(prefix):]
        if command in self._all_commands:
            return self._all_commands[command]

    def _get_args(self, command: Command, text: str) -> Optional[List[Any]]:
        if not command.args:
            return None

    def get_context(self, command: Command, message: discii.Message) -> Context:
        context = Context.from_message(command, message)
        return context

    async def process_commands(self, message: discii.Message):
        command = self._get_command(message.text)
        if command is None:
            return

        context = self.get_context(command, message)
        args = self._get_args(command, message.text)

        if args:
            await context.execute(context, args)
        else:
            await context.execute(context)

    async def _message_create(self, message: discii.Message) -> None:
        await self.process_commands(message)
