"""
computer_graphics_demo.fill
===========================

Fill a region.
"""
import copy


def cycle_shift(xs, number: int):
    """cycle_shift.

    :param xs:
    :param number:
    :type number: int
    """
    ys = copy.copy(xs)
    num = abs(number)
    for _ in range(num):
        if number < 0:
            ys.insert(0, ys.pop())
        else:
            ys.insert(len(ys), ys[0])
            ys.remove(ys[0])
    return ys
