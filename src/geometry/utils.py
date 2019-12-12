from typing import Tuple, Optional

import numpy as np

Point = Tuple[float, float]


def orient(a: np.ndarray, b: np.ndarray, c: np.ndarray) -> float:
    return a[0]*b[1] + b[0]*c[1] + c[0]*a[1] - a[0]*c[1] - b[0]*a[1] - c[0]*b[1]


def dist2(a: np.ndarray, b: np.ndarray) -> float:
    return sum(np.square(b - a))


def parametric_intersection(p1: Point, p2: Point, p3: Point, p4: Point) -> Optional[Tuple[float, float]]:
    """
    Finds parameters of intersection of two given lines (each defined by two points).
    Based on: http://www.cs.swan.ac.uk/~cssimon/line_intersection.html by Simon Walton.
    """

    # calculate values
    numerator1 = (p3[1] - p4[1]) * (p1[0] - p3[0]) + (p4[0] - p3[0]) * (p1[1] - p3[1])
    numerator2 = (p1[1] - p2[1]) * (p1[0] - p3[0]) + (p2[0] - p1[0]) * (p1[1] - p3[1])
    denominator = (p4[0] - p3[0]) * (p1[1] - p2[1]) - (p1[0] - p2[0]) * (p4[1] - p3[1])

    # if denominator is 0 then lines are parallel or are overlapping
    if denominator == 0:
        return None

    return numerator1 / denominator, numerator2 / denominator


def intersection(p1: Point, p2: Point, p3: Point, p4: Point,
                 restriction_1: str = 'line', restriction_2: str = 'line') -> Optional[Point]:
    """
    Returns intersection point (or None) of given (possibly restricted) lines.

    Possible line restrictions:
        - 'line' - no restriction, so its a line
        - 'segment' - restrictions on both ends, intersection has to be between given points
        - 'ray' - restriction on first point, intersection has to be on ray starting from first point
        - 'ray-inv' - restriction on second point, intersection has to be on ray starting from second point

    :param p1: first point of first line
    :param p2: second point of first line
    :param p3: first point of second line
    :param p4: second point of second line
    :param restriction_1: restriction for first line as describes above
    :param restriction_2: restriction for second line as describes above
    :return: intersection point or None
    """

    # get intersection parameters
    parameters = parametric_intersection(p1, p2, p3, p4)
    if parameters is None:
        return None
    t1, t2 = parameters

    # apply checks
    if restriction_1 in ['segment', 'ray'] and t1 < 0:
        return None
    if restriction_2 in ['segment', 'ray'] and t2 < 0:
        return None
    if restriction_1 in ['segment', 'ray-inv'] and t1 > 1:
        return None
    if restriction_2 in ['segment', 'ray-inv'] and t2 > 1:
        return None

    # return intersection point
    return (
        p1[0] + t1 * (p2[0] - p1[0]),
        p1[1] + t1 * (p2[1] - p1[1])
    )
