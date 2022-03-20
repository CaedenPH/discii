import discii
import sys
import traceback

from typing import TypeVar, Tuple, Optional, List, Dict, Coroutine, Callable, Any

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

    def command(self, *, names: List[str], enforce_types: bool = False) -> Any:
        """ """

        def inner(coro: Coro) -> Coro:
            coro._enforce_types = enforce_types
            command = Command(coro, names=names)

            for name in names:
                self._all_commands[name] = command

            return coro

        return inner

    def _get_command(self, text: str) -> Optional[Tuple[Command, List[str]]]:
        for prefix in self.prefixes:
            if text.startswith(prefix):
                break
        else:
            return None

        command = text[len(prefix) :].split()  # noqa: E203
        if command[0] in self._all_commands:
            return (self._all_commands[command[0]], command[1:])

    def _get_args(self, command: Command, message_args: List[str]) -> Optional[List[Any]]:
        if not command.args:
            return None

        if len(message_args) < len(
            [
                command.args[c]["optional"]
                for c in command.args
                if not command.args[c]["optional"]
            ]
        ):
            return None  # TODO: raise error

        args = []

        for (c, m) in zip(command.args, message_args):
            try:
                _type = command.args[c]["type"]
                args.append(_type(m))
            except Exception:
                return None  # TODO: raise error

        return args

    def get_context(self, command: Command, message: discii.Message) -> Context:
        context = Context.from_message(message, command)
        return context

    async def on_command_error(self, context: Context, error: Any) -> None:
        for handler in self.error_handlers["COMMAND"]:
            await handler(context, error)

    async def process_commands(self, message: discii.Message):
        command = self._get_command(message.text)
        if command is None:
            return

        (command, message_args) = command

        context = self.get_context(command, message)
        args = self._get_args(command, message_args) or ()

        try:
            await context.execute(*args)
        except Exception as e:
            await self.on_command_error(context, e)

    async def _message_create(self, message: discii.Message) -> None:
        await self.process_commands(message)
