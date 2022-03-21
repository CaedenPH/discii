# fmt: off
__all__ = (
    'DisciiException',
    'InvalidBotToken',
    'InvalidFunction',
    'SnowflakeNotFound',
    'UserNotFound',
    'ChannelNotFound',
)
# fmt: on


class DisciiException(Exception):
    """Base exception which all exceptions can inherit from."""


class InvalidBotToken(DisciiException):
    """Raised when the user inputs an invalid bot token."""


class InvalidFunction(DisciiException):
    """Raised when the user tries to register a non-asynchronous event."""


class SnowflakeNotFound(DisciiException):
    """Raised when a snowflake could not be found from the internat cache."""


class UserNotFound(SnowflakeNotFound):
    """Raised when a user could not be found."""


class ChannelNotFound(SnowflakeNotFound):
    """Raised when a user tried to get a non-existant channel."""


class InvalidArgumentType(DisciiException):
    """Raised when a command is called but ``enforce_types`` is ``True``
    and the argument types were invalid."""


class NotEnoughArguments(DisciiException):
    """Raised when a command is called but there weren't enough arguments passed
    into the command invokation."""
