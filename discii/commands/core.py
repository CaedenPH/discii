import inspect
import discii

from typing import Dict, List, Coroutine, Callable, Any


# fmt: off
__all__ = (
    'Command',
    'Context',
)
# fmt: on


def _parse_args(
    coro: Callable[..., Coroutine[Any, Any, Any]]
) -> List[Dict[str, Dict[str, Any]]]:
    signature = inspect.signature(coro)

    return [
        {param: signature.parameters[param].annotation}
        for param in signature.parameters
        if param not in "context"
    ]


class Command:
    def __init__(self, coro, *, names: List[str]) -> None:
        self.coro = coro
        self.args = _parse_args(coro)
        self.names = names


class Context(discii.Messageable):
    def __init__(self, *, command: Command, message: discii.Message) -> None:
        self.command = command
        self.message = message

    @classmethod
    def from_message(cls, command: Command, message: discii.Message):
        context = cls(command=command, message=message)
        return context

    async def _get_channel_id(self) -> int:
        return self.message.channel.id

    async def execute(self, *args):
        print(args)
        coro = self.command.coro

        try:
            await coro(*args)
        except Exception as e:
            print(e)
