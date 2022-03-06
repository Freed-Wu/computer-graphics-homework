"""
computer_graphics_demo.koch
===========================

Draw a Koch curve
"""
import math
from .line.bresenham import line


def rule(char: str) -> str:
    """rule.

    :param char:
    :type char: str
    :rtype: str
    """
    return "F+F--F+F" if char == "F" else char


def paint(R: int, G: int, B: int, scale: int, iteration_max: int, x0: int,
          y0: int):
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
    """
    info = "F"
    for _ in range(iteration_max):
        info = "".join(map(rule, info))
    x1, y1, angle = x0, y0, 0
    for char in info:
        if char == "F":
            x2 = x1 + scale * math.cos(angle)
            y2 = y1 + scale * math.sin(angle)
            line(R, G, B, math.floor(x1), math.floor(y1),
                 math.floor(x2), math.floor(y2))
            x1, y1 = x2, y2
        elif char == "+":
            angle += math.pi / 3
        elif char == "-":
            angle -= math.pi / 3
