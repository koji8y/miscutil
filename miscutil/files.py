"""File related uttilities."""
from typing import Any
from typing import Callable
from typing import Union

from contextlib import contextmanager
from contextlib import redirect_stderr
from contextlib import redirect_stdout
import gzip
from io import StringIO
from os import devnull
from pathlib import Path
import pickle
import sys


def pickledump(obj: Any, filename: Union[str, Path]) -> None:
    """dump object to pickle file."""
    filename_ = str(filename)
    if filename_.endswith(".gz"):
        with gzip.open(filename_, 'wb') as filestream:
            pickle.dump(obj, filestream)
        return
    with open(filename_, 'wb') as filestream:
        pickle.dump(obj, filestream)


def pickleload(filename: Union[str, Path]) -> Any:
    """load object from pickle file."""
    filename_ = str(filename)
    if filename_.endswith(".gz"):
        with gzip.open(filename_, 'rb') as filestream:
            return pickle.load(filestream)
    with open(filename_, 'rb') as filestream:
        return pickle.load(filestream)


@contextmanager
def suppress_stdout_stderr():
    """suppress stdout and stderr."""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


@contextmanager
def suppress_stderr_only():
    """suppress stderr."""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err:
            yield err


@contextmanager
def filter_stderr(is_line_to_be_suppressed: Callable[[str, str], bool]):
    """filter stderr."""
    output = StringIO()
    try:
        with redirect_stderr(output) as err:
            yield err
    finally:
        prev = ''
        for line in output.getvalue().split('\n'):
            try:
                if is_line_to_be_suppressed(line, prev):
                    continue
                print(line, file=sys.stderr)
            finally:
                prev = line
