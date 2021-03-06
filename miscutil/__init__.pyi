from pathlib import Path
from typing import Any, Callable, Iterable, Optional, TypeVar
from typing import Generic

TTT = TypeVar('TTT')
TTT2 = TypeVar('TTT2')

def none_or(value: Optional[TTT], convert: Callable[[TTT], TTT2], value_for_none: Optional[Callable[[], Optional[TTT2]]]=...) -> Optional[TTT2]: ...
def if_none(value: Optional[TTT], generate_alt: Callable[[], TTT]) -> TTT: ...
def ensure_not_none(value: Optional[TTT]) -> TTT: ...

class Entype(Generic[TTT]):
    @classmethod
    def coerce(cls: Any, elem: Any) -> TTT: ...

class DupableIterable(Iterable[TTT]):
    def __init__(self, es: Iterable[TTT]) -> None: ...
    def dup(self) -> Iterable[TTT]: ...
    def __iter__(self) -> Any: ...
    def __len__(self): ...

def nth_of(ordinal_number: int, default_value: Optional[TTT]=...) -> Callable[[Iterable[TTT]], Optional[TTT]]: ...
def nth(ordinal_number: int, elems: Iterable[TTT], default_value: Optional[TTT]=...) -> Optional[TTT]: ...
def head(count: int, elems: Iterable[TTT]) -> Iterable[TTT]: ...
def length(elems: Iterable[TTT]) -> int: ...
def missing(elems: Iterable[TTT]) -> bool: ...
def existing(elems: Iterable[TTT]) -> bool: ...
def ijoin(*args: TTT) -> Iterable[TTT]: ...
def to_end(elems: Iterable[TTT]) -> None: ...
def count_up() -> Iterable[int]: ...
def disj(boolfunc: Callable[[TTT], bool], elems: Iterable[TTT]) -> bool: ...
def conj(boolfunc: Callable[[TTT], bool], elems: Iterable[TTT], should_exist: bool=...) -> bool: ...
def imply(cond1: Callable[[], bool], cond2: Callable[[], bool]) -> bool: ...
def module_top() -> Path: ...
