import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sortedcontainers import SortedList

from src.geometry import intersection
from src.geometry.segments_intersections import Event, EventType
from src.visualization import plot_segments


class IntersectionsAnimation:
    """ Creates step-by-step animation of segments intersection detection. """

    def __init__(self, segments, frames):
        self.segments = segments
        self.frames = frames

        # init plot
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')

        plot_segments(segments)

        self.line_vertical = self.ax.axvline(color='r')
        self.scatter_events = self.ax.scatter([], [], color='r')
        self.scatter_intersections = self.ax.scatter([], [], color='g')

        # init animation
        self.animation = FuncAnimation(self.fig, self.animation_step, self.frames, self.animation_init, blit=True)

    def animation_init(self):
        self.scatter_events.set_offsets(np.empty((0, 2)))
        self.scatter_intersections.set_offsets(np.empty((0, 2)))
        self.line_vertical.set_xdata([0])
        return self.scatter_events, self.scatter_intersections, self.line_vertical

    def animation_step(self, frame):
        events, intersections, x = frame
        self.scatter_events.set_offsets(events or np.empty((0, 2)))
        self.scatter_intersections.set_offsets(intersections or np.empty((0, 2)))
        self.line_vertical.set_xdata([x])
        return self.scatter_events, self.scatter_intersections, self.line_vertical


def bentley_ottmann_generator(segments):
    """
    Bentley-Ottmann algorithm in form of a generator that yields next steps for animation.
    """

    # create queue of events
    events = SortedList()
    events.update(Event(min(*seg), EventType.BEGIN, (seg, )) for seg in segments)
    events.update(Event(max(*seg), EventType.END) for seg in segments)

    # create sweep line status
    status = SortedList()

    # intersections points
    result = set()

    # while there are events to handle
    while events:
        yield [e.point for e in events], list(result), events[0].point[0]

        event = events.pop(0)

        if event.type == EventType.BEGIN:
            for seg1 in event.segments:
                for seg2 in status:
                    point = intersection(*seg1, *seg2, restriction_1='segment', restriction_2='segment')
                    if point is not None and point not in result:
                        result.add(point)
                        events.add(Event(point, EventType.INTERSECTION))

            for seg in segments:
                status.add(seg)

        elif event.type == EventType.END:
            for seg in event.segments:
                status.remove(seg)

        elif event.type == EventType.INTERSECTION:
            pass

    yield [], list(result), 1000
