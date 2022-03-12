# fmt: off
__all__ = (
    'InvalidBotToken',
    'InvalidFunction',

)
# fmt: on


class InvalidBotToken(Exception):
    """Raised when the user inputs an invalid bot token."""


class InvalidFunction(Exception):
    """Raised when the user tries to register a non-asynchronous event."""
