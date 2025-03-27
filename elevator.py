from enum import Enum
from heapq import merge

class Door(Enum):
    """The door state."""

    OPEN = 1
    SHUT = 2

class Route:
    """A series of Elevator Stops in the same direction."""

    def __init__(self, start: int, end: int):
        """Initialize route with initial request details.

        :start: The start of the route
        :end: The end of the route
        """
        self.started = False
        self.up = start < end
        self.stops = [start, end]

    def start_if_ready(self, current: int) -> None:
        """Mark the route as started if th.

        Started routes can only grow up to the current level when merging.
        """
        self.started = (
            self.started
            or (self.up and current <= self.stops[0])
            or (not self.up and current >= self.stops[0])
        )

    def mergable(self, current_level: int, start: int, end: int) -> bool:
        """Return if route is eligible to be merged with requested start & end."""
        if self.up and self.started:
            return current_level <= start < end
        if self.up and not self.started:
            return start < end
        if not self.up and self.started:
            return current_level >= start > end
        return start > end

    def merge(self, start: int, end: int) -> None:
        """Merge the start and end levels into the route and remove duplicate stops."""
        if self.up:
            merged = list(merge(self.stops, [start, end]))
        else:
            merged = list(merge(self.stops, [start, end], reverse = True))
        self.stops = [merged[0]] + [
            stop for prev, stop
            in zip(merged, merged[1:])
            if prev != stop
        ]

    def next_stop(self) -> int:
        """Return the next stop."""
        return self.stops[0]

    def empty(self) -> bool:
        """Return true if there are no more stops in the route."""
        return not self.stops

    def pop(self) -> int:
        """Remove the current stop from the route."""
        return self.stops.pop(0)

class Elevator:
    """A single elevator which will move to requested levels and open/shut the door."""

    def __init__(self, level: int, door: Door = Door.SHUT):
        """Initialize Elevator with range and state.

        :floor: The floor this elevator is currently on
        :door: The state of the elevator door
        """
        self.level = level
        self.door = door
        self.routes = []

    def request(self, start: int, end: int) -> None:
        """Request that this elevator picks up a passenger.

        :start: where to pick up the passenger
        :end: where to drop off the passenger
        """
        if merge_route := next((
            r for r in self.routes
            if r.mergable(self.level, start, end)
        ), None):
            merge_route.merge(start, end)
        else:
            route = Route(start, end)
            if not self.routes:
                route.start_if_ready(self.level)
            self.routes.append(route)

    def move(self) -> None:
        """Allow an elevator to make one move according to it's stops.

        An elevator will either OPEN/CLOSE it's doors or move up/down a level
        """
        if self.door == Door.OPEN:
            self.door = Door.SHUT
        elif self.routes:
            route = self.routes[0]
            if route.next_stop() == self.level:
                self.door = Door.OPEN
                route.pop()
                if route.empty():
                    self.routes.pop(0)
                else:
                    route.start_if_ready(self.level)
            else:
                self.level += 1 if route.next_stop() > self.level else -1
