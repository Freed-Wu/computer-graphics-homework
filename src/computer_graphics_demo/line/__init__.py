"""
computer_graphics_demo.line
===========================

Draw a line.
"""
from ..fill import cycle_shift
from .. import setpixel
from typing import Callable, Optional


def polygon(
    R: int,
    G: int,
    B: int,
    *argv: int,
    isclose: bool = False,
    line: Optional[Callable[[int, int, int, int, int, int, int], None]] = None,
) -> None:
    """polygon.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param argv:
    :type argv: int
    :param isclose:
    :type isclose: bool
    :param line:
    :type line: Optional[Callable[[int, int, int, int, int, int, int], None]]
    :rtype: None
    """
    xs = argv[::2]
    ys = argv[1::2]
    if len(argv) % 2:
        exit(f"point number must be even, now is {len(argv)}")
    elif len(argv) % 2:
        exit(f"point number must be greater than 2, now is {len(xs)}")
    vertexs = list(zip(xs, ys))
    vertexs0 = cycle_shift(vertexs, -1)
    if isclose:
        edges = zip(vertexs0, vertexs)
    else:
        edges = zip(vertexs0[1:], vertexs[1:])
    for (x1, y1), (x2, y2) in edges:
        if line:
            line(R, G, B, x1, y1, x2, y2)
        else:
            setpixel(R, G, B, x1, y1)
            setpixel(R, G, B, x2, y2)
