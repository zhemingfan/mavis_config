import os
from contextlib import contextmanager


@contextmanager
def not_raises(ExpectedException):
    # credit: https://gist.github.com/oisinmulvihill/45c14271fad7794a4a52516ecb784e69
    try:
        yield

    except ExpectedException as error:
        raise AssertionError(f"Raised exception {error} when it should not!")

    except Exception as error:
        raise AssertionError(f"An unexpected exception {error} raised.")


def package_path(*paths):
    return os.path.join(os.path.dirname(__file__), '..', *paths)
