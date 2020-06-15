"""miscelaneas utilities."""
from typing import Any
from typing import Callable
from typing import Generic
from typing import Iterable
from typing import Optional
from typing import TypeVar

from functools import reduce
from itertools import tee
from pathlib import Path

__version__ = '0.10.1'


TTT = TypeVar('TTT')
TTT2 = TypeVar('TTT2')


def none_or(value: Optional[TTT],
            convert: Callable[[TTT], TTT2],
            value_for_none: Optional[
                Callable[[], Optional[TTT2]]] = None) -> Optional[TTT2]:
    """get converted value if other than None is passed."""
    return ((None if value_for_none is None else value_for_none())
            if value is None else convert(value))


def if_none(value: Optional[TTT], generate_alt: Callable[[], TTT]) -> TTT:
    """supply alternate value if None is passed."""
    return generate_alt() if value is None else value


def ensure_not_none(value: Optional[TTT]) -> TTT:
    """ensure the value is not None."""
    assert value is not None
    return value


class Entype(Generic[TTT]):  # pylint: disable=too-few-public-methods
    """collection of type coerciion method."""
    @classmethod
    def coerce(cls, elem: Any) -> TTT:
        """coerce type."""
        return elem


class DupableIterable(Iterable[TTT]):
    """Duplicatable class of Iterable."""
    def __init__(self, es: Iterable[TTT]):
        self._iter: Iterable[TTT] = es

    def dup(self) -> Iterable[TTT]:
        """duplicate this Iterable."""
        to_return, self._iter = tee(self._iter)
        return to_return

    def __iter__(self):
        return self.dup()

    def __len__(self):
        count = 0
        for _ in self:
            count += 1
        return count


def nth_of(ordinal_number: int,
           default_value: Optional[TTT] = None) -> (
               Callable[[Iterable[TTT]], Optional[TTT]]):
    """obtain a function to get nth element."""
    def _get(elems: Iterable[TTT]) -> Optional[TTT]:
        return nth(ordinal_number, elems, default_value)
    return _get


def nth(ordinal_number: int,
        elems: Iterable[TTT],
        default_value: Optional[TTT] = None) -> Optional[TTT]:
    """要素の並び elems の中の ordinal_number 番目の要素を返す．

    先頭は 0 番．
    """

    if ordinal_number < 0:
        elems_dup = DupableIterable(elems)
        _length = len(elems_dup)
        return nth(_length - ordinal_number, elems_dup, default_value)

    idx = 0
    for elem in elems:
        if idx == ordinal_number:
            return elem
        idx += 1

    if default_value is not None:
        return default_value
    return None


def head(count: int, elems: Iterable[TTT]) -> Iterable[TTT]:
    """get first `count` elements."""
    idx = 0
    for elem in elems:
        if idx >= count:
            break
        idx += 1
        yield elem


def length(elems: Iterable[TTT]) -> int:
    """count elements in iterable."""
    return reduce(lambda result, elem: result + 1, DupableIterable(elems), 0)


def missing(elems: Iterable[TTT]) -> bool:
    """elems が 0 個なら True を返す．"""

    return nth(0, elems) is None


def existing(elems: Iterable[TTT]) -> bool:
    """elems が 1 個以上なら True を返す．"""

    return nth(0, elems) is not None


def ijoin(*args: TTT) -> Iterable[TTT]:
    """名前なしパラメタ列から generator を作る．"""
    yield from args


def to_end(elems: Iterable[TTT]) -> None:
    """enumerate elements to the end."""
    for _ in elems:
        pass


def count_up() -> Iterable[int]:
    """count up eternaly."""
    num: int = 0
    while True:
        yield num
        num += 1


def disj(boolfunc: Callable[[TTT], bool], elems: Iterable[TTT]) -> bool:
    """Disjunction. いずれかが成り立てば True を返す．

    Parameters:
      boolfunc: object->bool - 要素を真偽値に変換する関数．
      elems - 要素の並び．
    """
    for elem in elems:
        if boolfunc(elem):
            return True
    return False


def conj(boolfunc: Callable[[TTT], bool],
         elems: Iterable[TTT],
         should_exist: bool = False) -> bool:
    """Conjunction. 全てが成り立てば True を返す．

    Paremeters:
      boolfunc: object->bool - 要素を真偽値に変換する関数．
      elems - 要素の並び．
    """
    exists = False
    for elem in elems:
        if not boolfunc(elem):
            return False
        exists = True
    return imply(lambda: should_exist, lambda: exists)


def imply(cond1: Callable[[], bool], cond2: Callable[[], bool]) -> bool:
    """「cond1() ならば cond2()」の真偽値を返す．"""
    return (not cond1()) or cond2()


def module_top() -> Path:
    """get top folder path of this module."""
    # return Path(if_none(nth(0, __path__), lambda: ".")).parent
    try:
        # pylint: disable=eval-used
        return Path(eval('__spec__').origin).parent.parent
    except NameError:
        return Path('.')
