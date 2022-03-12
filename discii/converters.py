from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message
    from .state import ClientState


def _event_to_object(name: str, data: Dict[Any, Any], _state: "ClientState") -> Any:
    _event_converters: Dict[str, Any] = {"READY": None, "MESSAGE": Message}

    if name not in _event_converters:
        return None

    converter = _event_converters[name]
    if converter is None:
        return None

    state = converter(payload=data, state=_state)
    return state
