"""
computer_graphics_demo.fill.scan
================================

Scan line algorithm.
"""
import taichi as ti
from typing import List, Tuple, Optional
from .. import setpixel
from . import cycle_shift


def paint(R: int, G: int, B: int, *argv: int):
    """paint.

    :param R:
    :type R: int
    :param G:
    :type G: int
    :param B:
    :type B: int
    :param argv:
    :type argv: int
    """
    if len(argv) % 2:
        exit(f"point number must be even, now is {len(argv)}")
    elif len(argv) < 6:
        exit(f"point number must be greater than 3, now is {len(argv)}")
    xs = argv[::2]
    ys = argv[1::2]
    vertexs = list(zip(xs, ys))
    y_max = max(ys)
    vertexs0 = cycle_shift(vertexs, -1)
    vertexs2 = cycle_shift(vertexs, 1)
    vertexs3 = cycle_shift(vertexs2, 1)
    edges = zip(vertexs0, vertexs, vertexs2, vertexs3)  # type: ignore
    edge_table: List[Optional[List[Tuple[int, float, float]]]] = [None] * y_max

    # sorted edge table
    for (_, y0), (x1, y1), (x2, y2), (_, y3) in edges:
        if y1 == y2:
            continue
        dx = (x2 - x1) / (y2 - y1)
        ymin, ymax = ti.min(y1, y2), ti.max(y1, y2)
        if ymin == y1:
            xstart = x1 + 0.0
        else:
            xstart = x2 + 0.0
        # https://github.com/jingedawang/PolygonScan/blob/master/main.cpp#L109
        if y0 < y1 < y2 or y1 > y2 > y3:
            ymin += 1
            xstart += dx
        if edge_table[ymin]:
            edge_table[ymin] += [(ymax, xstart, dx)]  # type: ignore
        else:
            edge_table[ymin] = [(ymax, xstart, dx)]

    # active edge table
    edge_list_old = None
    for y in range(y_max):
        if edge_list_old:
            for ymax, xstart, dx in edge_list_old:
                if y <= ymax:
                    if edge_table[y]:
                        edge_table[y] += [(ymax, xstart + dx, dx)]
                        edge_table[y] = sorted(
                            edge_table[y], key=lambda x: x[2]  # type: ignore
                        )
                        edge_table[y] = sorted(
                            edge_table[y], key=lambda x: x[1]  # type: ignore
                        )
                    else:
                        edge_table[y] = [(ymax, xstart + dx, dx)]
        if edge_table[y]:
            edge_list_old = edge_table[y]
            for i in range(len(edge_table[y])):  # type: ignore
                if i % 2 == 1:
                    continue
                x_start = ti.ceil(edge_table[y][i][1])  # type: ignore
                x_end = ti.floor(edge_table[y][i + 1][1]) + 1  # type: ignore
                for x in range(x_start, x_end):
                    setpixel(x, y, R, G, B)
