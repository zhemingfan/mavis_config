from typing import List


class EnumType(type):
    def __contains__(cls, member):
        return member in cls.values()

    def __getitem__(cls, item):
        for k, v in cls.items():
            if k == item:
                return v
        raise KeyError(item)

    def __iter__(cls):
        """
        Returns members in definition order.
        """
        return iter(cls.values())

    def __len__(cls):
        return len(cls.values())


class MavisNamespace(metaclass=EnumType):
    @classmethod
    def items(cls):
        return [(k, v) for k, v in cls.__dict__.items() if not k.startswith('_')]

    @classmethod
    def to_dict(cls):
        return dict(cls.items())

    @classmethod
    def keys(cls):
        return [k for k, v in cls.items()]

    @classmethod
    def values(cls):
        return [v for k, v in cls.items()]

    @classmethod
    def enforce(cls, value):
        """
        checks that the current namespace has a given value

        Returns:
            the input value

        Raises:
            KeyError: the value did not exist

        Example:
            >>> nspace.enforce(1)
            1
            >>> nspace.enforce(3)
            Traceback (most recent call last):
            ....
        """
        if value not in cls.values():
            raise KeyError('value {0} is not a valid member of '.format(repr(value)), cls.values())
        return value

    @classmethod
    def reverse(cls, value):
        """
        for a given value, return the associated key

        Args:
            value: the value to get the key/attribute name for

        Raises:
            KeyError: the value is not unique
            KeyError: the value is not assigned

        Example:
            >>> nspace.reverse(1)
            'thing'
        """
        for key in cls.keys():
            if cls[key] == value:
                return key
        raise KeyError(f'input value ({value}) is not assigned to a key')


class SUBCOMMAND(MavisNamespace):
    """
    holds controlled vocabulary for allowed pipeline stage values
    """

    ANNOTATE: str = 'annotate'
    VALIDATE: str = 'validate'
    CLUSTER: str = 'cluster'
    PAIR: str = 'pairing'
    SUMMARY: str = 'summary'
    CONVERT: str = 'convert'
    OVERLAY: str = 'overlay'
    SETUP: str = 'setup'
