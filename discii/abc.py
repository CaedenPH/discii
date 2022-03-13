__all__ = ("Snowflake",)


class Snowflake:
    """
    The abstract snowflake which all models
    and objects will inherit from.

    Attributes
    ----------
    id: :class:`int`
        The id that the snowflake has.
    """

    id: int
