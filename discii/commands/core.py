import inspect
import discii
import discii.abc as _abc

from typing import TYPE_CHEKCING, Dict, List, Coroutine, Callable, Any

if TYPE_CHECKING:
    from discii.state import ClientState 

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
     """
     Represents a command.
     
     Parameters
     ----------
     coro: :class:`Callable[..., Coroutine[Any, Any, Any]]`
        The coroutine function that is 
        bound to the command. Similiar to 
        event bindings.
     names: :class:`List[str]`
        The names that the command is invokable 
        from.
     """
        
    def __init__(self, coro: Callable[..., Coroutine[Any, Any, Any]], *, names: List[str]) -> None:
        self.coro = coro
        self.args: Dict[str, Dict[str, Any]] = _parse_args(coro)
        self.names = names


class Context(_abc.Messageable, _abc.Repliable):
    """
    Represents a `Context` object.
    
    Parameters
    ----------
    message: :class:`discii.Message`
        The message object that is bound 
        to the context instance.
    command: :class:`Command`
        The command bound to the context
        instance.
    
    Attributes
    ----------
    _state: :class:`ClientState`
        The client state which methods can be 
        called off of.  
    """
    _state: "ClientState"
        
        
    def __init__(self, *, message: discii.Message, command: Command) -> None:
        self.command = command
        self.message = message

    @classmethod
    def from_message(cls, message: discii.Message, command: Command):
        context = cls(message=message, command=command)
        context._state = message._state
        return context

    async def _get_channel_id(self) -> int:
        return self.message.channel.id

    async def execute(self, *args):
        coro = self.command.coro
        await coro(*args)
