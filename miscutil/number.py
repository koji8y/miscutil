"""utilities for numbers."""
from typing import Any
from typing import Callable
from typing import Iterable

import statistics

import numpy as np  # type: ignore

from miscutil import DupableIterable


NAN = float('nan')


def nnan(nums: Iterable[float]) -> Iterable[float]:
    """omit NaN from float numbers."""
    return DupableIterable(num for num in nums if not np.isnan(num))


def nan_if_error(func: Callable[[Any], float], data: Any) -> float:
    """function wrapper to convert exception to nan emission."""
    try:
        return func(data)
    except (statistics.StatisticsError, ValueError):
        return NAN


# def safe_max(
#        num: Optional[Union[float, Iterable[float]]] = None,
#        *nums: float) -> float:
#    """max function that emits nan instead of raising an exception."""
#    try:
#        if num is None:
#            return float('nan')
#        if isinstance(num, float):
#            return max(num, *nums)
#        return max(*num, *nums)
#    except ValueError:
#        return float('nan')


def safe_max(*args: Any, **kwargs: Any) -> float:
    """max function that emits nan instead of raising an exception."""
    try:
        return max(*args, **kwargs)
    except (TypeError, ValueError):
        return NAN
