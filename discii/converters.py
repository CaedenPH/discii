from typing import Any, Dict, TYPE_CHECKING

from .message import Message

if TYPE_CHECKING:
    from .state import ClientState


def _event_to_object(name: str, data: Dict[Any, Any], _state: "ClientState") -> Any:
    _event_converters: Dict[str, Any] = {"READY": None, "MESSAGE_CREATE": Message}

    if name not in _event_converters:
        return None

    converter = _event_converters[name]
    if converter is None:
        return None

    state = converter(payload=data, client_state=_state)
    return (state,)
