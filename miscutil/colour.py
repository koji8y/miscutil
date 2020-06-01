"""Utilities for colourization."""
from typing import List

from colour import Color  # type: ignore


def color_range(start_color: str, goal_color: str, count: int) -> List[str]:
    """get color range."""
    return [col.get_hex_l()
            for col in Color(start_color).range_to(Color(goal_color), count)]
