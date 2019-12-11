import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sortedcontainers import SortedList

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
    Bentley-Ottmann algorithm in for of a generator that yields next steps for animation.
    """

    # create segments from given data
    segments = [(tuple(a), tuple(b)) for a, b in segments]

    # create queue of events
    events = SortedList()
    events.update(Event(min(*seg), EventType.BEGIN, seg) for seg in segments)
    events.update(Event(max(*seg), EventType.END) for seg in segments)

    # create sweep line status
    status = SortedList()

    # while there are events to handle
    while events:
        yield [e.point for e in events], [], events[0].point[0]

        # get next event to handle
        event = events.pop(0)

        if event.type == EventType.END:
            # add segment to line status
            status.add(event.segments[0])


        elif event.type == EventType.BEGIN:
            pass
        elif event.type == EventType.INTERSECTION:
            pass
