from dataclasses import dataclass, field
from enum import Enum
from heapq import heapify, heappop
from typing import Tuple

from sortedcontainers import SortedList

from src.geometry import intersection

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
    """ Bentley-Ottmann algorithm implementation. """

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

        event = events.pop(0)

        if event.type == EventType.BEGIN:
            for seg1 in event.segments:
                for seg2 in status:
                    point = intersection(*seg1, *seg2, restriction_1='segment', restriction_2='segment')
                    if point is None:
                        continue
                    point = (round(point[0], 15), round(point[1], 15))
                    if point not in result:
                        result.add(point)
                        events.add(Event(point, EventType.INTERSECTION))

            for seg in event.segments:
                status.add(seg)

        elif event.type == EventType.END:
            for seg in event.segments:
                status.remove(seg)

        elif event.type == EventType.INTERSECTION:
            pass

    return result
