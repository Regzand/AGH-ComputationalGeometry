from dataclasses import dataclass, field
from enum import Enum
from heapq import heapify, heappop
from typing import Tuple

Point = Tuple[float, float]
Segment = Tuple[Point, Point]


class EventType(Enum):
    """ Defines type of event point. """
    BEGIN = 0
    INTERSECTION = 1
    END = 2


@dataclass(order=True)
class Event:
    """ Defines event point. """
    point: Point
    type: EventType
    segments: Tuple[Segment, ...] = field(compare=False, default_factory=tuple)


def bentley_ottmann(segments):

    # create segments from given data
    segments = [(tuple(a), tuple(b)) for a, b in segments]

    # create heap queue of events
    events = [Event(min(*seg), EventType.BEGIN, seg) for seg in segments]
    events += [Event(max(*seg), EventType.END) for seg in segments]
    heapify(events)

    # while there are events to handle
    while events:
        event = heappop(events)


