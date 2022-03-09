import json
from typing import Any

try:
    import orjson
except ImportError:
    HAS_ORJSON = False
else:
    HAS_ORJSON = True

if HAS_ORJSON:

    def _to_json(obj: Any) -> str:  # type: ignore
        return orjson.dumps(obj).decode("utf-8")

    _from_json = orjson.loads  # type: ignore

else:

    def _to_json(obj: Any) -> str:
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=True)

    _from_json = json.loads
