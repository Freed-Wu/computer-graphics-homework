"""
computer_graphics_demo.b
========================

Draw a B-spline.
"""
import taichi as ti
from .line import polygon
from .line.bresenham import line
from typing import List

nodes = [0, 0, 0, 0, 100, 200, 300, 400, 500, 500, 500, 500]


def b_basis(i: int, degree: int, u: int, nodes: List[int]) -> float:
    """b_basis.

    :param i:
    :type i: int
    :param degree:
    :type degree: int
    :param u:
    :type u: int
    :param nodes:
    :type nodes: List[int]
    :rtype: float
    """
    if degree:
        length1 = nodes[i + degree] - nodes[i]
        length2 = nodes[i + degree + 1] - nodes[i + 1]
        alpha = (u - nodes[i]) / length1 if length1 else 0
        beta = (nodes[i + degree + 1] - u) / length2 if length2 else 0
        result = alpha * b_basis(i, degree - 1, u, nodes) + beta * b_basis(
            i + 1, degree - 1, u, nodes
        )
    else:
        result = float(nodes[i] < u <= nodes[i + 1])
    return result


def paint(R: int, G: int, B: int, degree: int, *argv: int) -> None:
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param degree:
    :type degree: int
    :param argv:
    :type argv: int
    :rtype: None
    """
    xs = argv[::2]
    ys = argv[1::2]
    if len(argv) % 2:
        exit(f"point number must be even, now is {len(argv)}")
    elif len(argv) < 6:
        n_node = len(xs) + degree + 1
        exit(f"node number must be greater than {n_node}, now is {len(nodes)}")
    argv2 = []
    for u in range(nodes[0], nodes[-1]):
        x, y = 0, 0
        for i in range(len(xs)):
            x += xs[i] * b_basis(i, degree, u, nodes)
            y += ys[i] * b_basis(i, degree, u, nodes)
        argv2 += [ti.floor(x), ti.floor(y)]
    polygon(R, G, B, *argv2, line=line)
