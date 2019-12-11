from collections import defaultdict

from src.geometry import orient


def to_polygon(lines):
    return [line[0] for line in lines]


def classify_vertex(a, b, c):
    if a[1] < b[1] and c[1] < b[1]:
        if orient(a, b, c) > 0:
            return "begin"
        else:
            return "split"
    if a[1] > b[1] and c[1] > b[1]:
        if orient(a, b, c) > 0:
            return "end"
        else:
            return "connect"
    return "correct"


def classify_poly(points):
    classes = defaultdict(list)

    for i in range(len(points)):
        classes[classify_vertex(points[i - 2], points[i - 1], points[i])].append((i - 1 + len(points)) % len(points))

    return classes


def is_y_monotonic(poly):
    classification = classify_poly(poly)
    return not classification['connect'] and not classification['split']


def poly_to_two_chains(poly):
    classification = classify_poly(poly)
    start = classification['begin'][0]
    end = classification['end'][0]

    if start < end:
        left = poly[start:end+1]
        right = poly[end:] + poly[:start+1]
    else:
        right = poly[end:start+1]
        left = poly[start:] + poly[:end+1]
    return left, right


def triangulate_monotonic(poly):

    # get two chains
    left, right = poly_to_two_chains(poly)

    # sort chains
    left = sorted(left, key=lambda p: p[1], reverse=True)
    right = sorted(right, key=lambda p: p[1], reverse=True)

    # result
    result = []

    # visible vertices
    visible = [left[0]]

    # for each event
    il = 1
    ir = 0
    while il < len(left) - 1 or ir < len(right) - 1:

        # select side and get event
        if left[il][1] > right[ir][1]:
            side = 'left'
            e = left[il]
            il += 1
        else:
            side = 'right'
            e = right[ir]
            ir += 1

        # holds list of vertices that block other vertices
        blocking = []

        # get previous on this side
        if side == 'left':
            prev = left[il-2] if il > 1 else left[0]
        else:
            prev = right[ir-2] if ir > 1 else left[0]

        # for each visible point
        for v in visible:

            if v != prev:
                if side == 'left' and orient(e, prev, v) > 0:
                    continue
                if side == 'right' and orient(e, prev, v) < 0:
                    continue

            result.append((v, e))

            # if its a line from left to right it blocks
            if (v in left and e in right) or (v in right and e in left):
                blocking.append(v)

        # update visible vertices
        if blocking:
            visible = [min(blocking, key=lambda x: x[1])]
        visible.append(e)

    # add end vertex
    for v in visible:
        result.append((v, left[-1]))

    return result
