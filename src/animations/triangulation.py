import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

from src.geometry import poly_to_two_chains, orient
from src.visualization import plot_chain, plot_points
from matplotlib.animation import FuncAnimation


class TriangulationAnimation:
    """ Creates step-by-step animation of triangulation. """

    def __init__(self, poly, frames):
        self.poly = poly
        self.frames = frames

        # init plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')

        plot_chain(self.poly, closed=True)
        plot_points(self.poly)

        self.line_horizontal = self.ax.axhline(0, color='r')
        self.lines_result = LineCollection([], colors='g')
        self.ax.add_collection(self.lines_result)

        # init animation
        self.animation = FuncAnimation(self.fig, self.animation_step, self.frames, self.animation_init, blit=True)

    def animation_init(self):
        self.line_horizontal.set_ydata([0])
        self.lines_result.set_segments([])
        return self.line_horizontal,

    def animation_step(self, frame):
        y, result = frame
        self.line_horizontal.set_ydata([y])
        self.lines_result.set_segments(result)
        return self.line_horizontal,


def triangulate_monotonic_generator(poly):

    # get two chains
    left, right = poly_to_two_chains(poly)

    yield (left[0][1], [])

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

        yield(e[1], result)

    # add end vertex
    for v in visible:
        result.append((v, left[-1]))

    yield (left[-1][1], result)
    yield (-100, result)
