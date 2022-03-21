import asyncio
import discii
import sys
import traceback

from typing import TypeVar, Tuple, Optional, List, Dict, Coroutine, Callable, Any

from discii.errors import InvalidFunction, InvalidArgumentType, NotEnoughArguments
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

    Parameters
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

    def error(self, *, command: bool = False) -> Any:
        """
        Overrides the default error handler.

        Parameters
        ----------
        command: :class:`bool`
            Registers the error handler as a
            command error handler. Only compatible
            for `Bot` instances.
        """

        def inner(coro: Coro) -> Coro:
            if not asyncio.iscoroutinefunction(coro):
                raise InvalidFunction("Your event must be a coroutine.")

            if command:
                setattr(self, "on_command_error", coro)
            else:
                setattr(self, "on_error", coro)

            return coro

        return inner

    def command(self, *, names: List[str], enforce_types: bool = False) -> Any:
        """
        A decorator that registers commands
        to the bot.

        Parameters
        ----------
        names: :class:`List[str]`
            The names that the command is
            invoked by.
        enforce_types: :class:`bool`
            Whether or not to enforce types
            when calling the function
        """

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
            raise NotEnoughArguments

        args = []

        for (c, m) in zip(command.args, message_args):
            try:
                _type = command.args[c]["type"]
                args.append(_type(m))
            except Exception:
                raise InvalidArgumentType

        return args

    async def _message_create(self, message: discii.Message) -> None:
        await self.process_commands(message)

    def get_context(self, command: Command, message: discii.Message) -> Context:
        """
        Returns a context instance from a
        message and command object.

        Parameters
        ----------
        command: :class:`Command`
            The command that is bound to the
            context.
        message: :class:`discii.Message`
            The message object to attach
            to the context.

        Returns
        -------
        context: :class:`Context`
            The context created from the message and
            command.
        """

        context = Context.from_message(message, command)
        return context

    async def on_command_error(self, context: Context, error: Any) -> None:
        """
        Default error handler that dispatches the
        errors to the error_handlers.
        """

        print(
            f"Exception in :command:``{context.command.coro.__name__}``", file=sys.stderr
        )
        traceback.print_exc()

    async def process_commands(self, message: discii.Message):
        """
        Processes a command from a message object.

        Parameters
        ----------
        message: :class:`discii.Message`
            The message object.
        """

        command = self._get_command(message.text)
        if command is None:
            return

        (command, message_args) = command

        context = self.get_context(command, message)
        args = self._get_args(command, message_args) or ()

        try:
            await context.execute(context, *args)
        except Exception as e:
            await self.on_command_error(context, e)
