from enum import Enum

class Building:

    """A Building has a collection of floors and elevators.

    Make a #request for an elevator and #wait for the elevators to move.
    """

    def __init__(self, top: int, bottom: int, elevators: list):
        """Initialize Building with elevators servicing all floors.

        :top: The top floor of the building
        :bottom: The bottom floor of the building
        :elevators: A list of where all the elevators are
        """
        self.elevators = [
            Elevator(top=top, bottom=bottom, floor=floor)
            for floor in elevators
        ]

    def request(self, start: int, end: int) -> None:
        """Send a request for an elevator to stop at a particular floor.

        :start: The floor the elevator will pick up passengers from
        :end: The floor the elevator will drop passengers at
        """
        self.elevators[0].request(start = start, end = end)

    def wait(self, ticks: int = 1)-> None:
        """Wait for the elevators to move.

        :ticks: The amount of elevator movements to wait. default = 1
        """
        for _ in range(ticks):
            for elevator in self.elevators:
                elevator.move()

class Door(Enum):
    """The door state."""

    OPEN = 1
    SHUT = 2

class Elevator:
    """A single elevator which will move to target levels and Open/shut the door."""

    def __init__(self, top: int, bottom: int, floor: int, door: Door = Door.SHUT):
        """Initialize Elevator with range and state.

        :top: The top floor this elevator goes to
        :bottom: The bottom floor this elevator goes to
        :floor: The floor this elevator is currently on
        :door: The state of the elevator door
        """
        self.floor = floor
        self.top = top
        self.bottom = bottom
        self.door = door
        self.targets = []

    def request(self, start: int, end: int) -> None:
        """Request that this elevator picks up a passenger.

        :start: where to pick up the passenger
        :end: where to drop off the passenger
        """
        self.targets.extend([start, end])

    def move(self) -> None:
        """Allow an elevator to make one move according to it's targets.

        An elevator will either OPEN/CLOSE it's doors or move up/down a level
        """
        if self.door == Door.OPEN:
            self.door = Door.SHUT
        elif self.targets:
            target = self.targets[0]
            if target == self.floor:
                self.door = Door.OPEN
                self.targets.pop(0)
            else:
                self.floor +=  1 if target > self.floor else -1
