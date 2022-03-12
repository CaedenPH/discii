from typing import Any, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from .state import ClientState


def _event_to_state(name: str, data: Dict[Any, Any], client_state: "ClientState") -> Any:
    _event_converters = {
        "READY": None,
    }

    if name not in _event_converters:
        return None

    converter = _event_converters[name]
    if converter is None:
        return None
