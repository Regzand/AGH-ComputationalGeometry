from functools import cmp_to_key, partial

import numpy as np

from code.geometry import orient, dist2


def graham(points: np.ndarray, epsilon: float = 1e-10):

    # find first point (with lowest y then x) and remove it from points
    i0 = min(enumerate(points), key=lambda x: (x[1][1], x[1][0]))[0]
    p0 = points[i0]
    points = points[np.arange(points.shape[0]) != i0]

    # sort points by orient relative to p0
    points = sorted(points, key=cmp_to_key(partial(orient, p0)), reverse=True)

    # remove points that are co-linear
    i = 0
    while i < len(points)-1:
        # if they are not co-linear continue
        if abs(orient(p0, points[i], points[i+1])) > epsilon:
            i += 1
        # if they are co-linear and i is closer then i+1
        elif dist2(p0, points[i]) < dist2(p0, points[i+1]):
            del points[i]
        # if they are co-linear and i+1 is closer than i
        else:
            del points[i+1]

    # initialize stack
    hull = [p0]

    # main loop
    i = 0
    while i < len(points):
        # if its on the right
        if len(hull) < 2 or orient(hull[-2], hull[-1], points[i]) > epsilon:
            hull.append(points[i])
            i += 1
        # if its on the left
        else:
            hull.pop()

    return hull


def jarvis(points: np.ndarray, epsilon: float = 1e-10):

    # find first point (with lowest y then x)
    p0 = points[min(enumerate(points), key=lambda x: (x[1][1], x[1][0]))[0]]

    # init hull
    hull = [p0]

    # main loop
    for i in range(len(points)):

        # find right most point relative to last in hull
        best = None
        for p in points:

            # if there is no best
            if best is None:
                best = p
            # if p is more to the right than best
            elif orient(hull[-1], best, p) < -epsilon:
                best = p
            # if p and best are co-linear and best is closer than p
            elif -epsilon < orient(hull[-1], best, p) < epsilon and dist2(hull[-1], best) < dist2(hull[-1], p):
                best = p

        # stop main loop if hull is closed
        if np.all(best == hull[0]):
            break

        # add found point to hull
        hull.append(best)

    return hull

