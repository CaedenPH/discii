import inspect
import discii
import discii.abc as abc

from typing import Dict, List, Coroutine, Callable, Any


# fmt: off
__all__ = (
    'Command',
    'Context',
)
# fmt: on


def _parse_args(
    coro: Callable[..., Coroutine[Any, Any, Any]]
) -> Dict[str, Dict[str, Any]]:
    signature = inspect.signature(coro)

    args = {}
    for param in signature.parameters:
        if param not in "context":
            args[param] = {
                "type": signature.parameters[param].annotation,
                "optional": False
                if signature.parameters[param].default is inspect._empty
                else True,
            }
    return args


class Command:
    def __init__(self, coro, *, names: List[str]) -> None:
        self.coro = coro
        self.args: Dict[str, Dict[str, Any]] = _parse_args(coro)
        self.names = names


class Context(abc.Messageable, abc.Repliable):
    def __init__(self, *, message: discii.Message, command: Command) -> None:
        self.command = command
        self.message = message
        self._state = message._state

    @classmethod
    def from_message(cls, message: discii.Message, command: Command):
        context = cls(command=command, message=message)
        return context

    async def _get_channel_id(self) -> int:
        return self.message.channel.id

    async def execute(self, *args):
        coro = self.command.coro
        await coro(*args)
