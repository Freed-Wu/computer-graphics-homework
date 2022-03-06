"""
computer_graphics_demo.fern
===========================

Draw a fern.
"""
import taichi as ti
import numpy as np
from . import setpixel
from typing import List, Tuple

# https://en.wikipedia.org/wiki/Barnsley_fern
probability = [0.01, 0.07, 0.07, 0.85]
# means x[n + 1] = np.dot(pos, eq)
# where pos = [x[n], y[n], 1]
# y[n + 1] ditto
eqs = [
    np.array([[0, 0, 0], [0, 0.16, 0]]),
    np.array([[0.2, -0.26, 0], [0.23, 0.22, 1.6]]),
    np.array([[-0.15, 0.28, 0], [0.26, 0.24, 0.44]]),
    np.array([[0.85, 0.04, 0], [-0.04, 0.85, 1.6]]),
]


def fern(
    probability: List[float],
    eqs: List[np.ndarray],
    init: List[float],
    iteration_max: int,
) -> Tuple[List[float], List[float]]:
    """fern.

    :param probability:
    :type probability: List[float]
    :param eqs:
    :type eqs: List[np.ndarray]
    :param init:
    :type init: List[float]
    :param iteration_max:
    :type iteration_max: int
    :rtype: Tuple[List[float], List[float]]
    """
    pos = np.ones(3, dtype=float)
    pos[: len(init)] = init
    probability = np.add.accumulate(probability)  # type: ignore
    rands = np.random.rand(iteration_max)
    select = np.zeros(iteration_max, dtype=int)
    for i, p in enumerate(probability):
        select[rands < p] = i
        # mark these indice has been used
        rands[rands < p] = 1

    xs, ys = [], []
    for i in range(iteration_max):
        tmp = np.dot(eqs[select[i]], pos)
        pos[:2] = tmp
        xs += [tmp[0]]
        ys += [tmp[1]]

    return xs, ys


def paint(
    R: int, G: int, B: int, scale: int, iteration_max: int, x0: int, y0: int
) -> None:
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param scale:
    :type scale: int
    :param iteration_max:
    :type iteration_max: int
    :param x0:
    :type x0: int
    :param y0:
    :type y0: int
    :rtype: None
    """
    xs, ys = fern(probability, eqs, [0] * 2, iteration_max)
    for x, y in zip(xs, ys):
        x1, y1 = x0 + ti.floor(x * scale), y0 + ti.floor(y * scale)
        setpixel(x1, y1, R, G, B)
