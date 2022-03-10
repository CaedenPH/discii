class InvalidToken(Exception):
    """Exception raised when an invalid token has been passed into Client."""


class InvalidFunction(Exception):
    """Exception raised when a user tried to decorate a non-asynchronous functions."""
