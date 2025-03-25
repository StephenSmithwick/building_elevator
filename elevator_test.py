from elevator import Door, Elevator


class TestElevator:
    def test_elevator_request_adds_a_targetfor_start_and_end(self):
        elevator = Elevator(floor=0, top=20, bottom=-2)
        elevator.request(start = -1, end = 0)

        assert elevator.floor == 0
        assert elevator.door == Door.SHUT
        assert elevator.targets == [-1, 0]

    def test_elevator_opens_door_on_target(self):
        elevator = Elevator(floor=0, top=20, bottom=-2, door=Door.SHUT)
        elevator.request(start = 0, end = 1)

        elevator.move()

        assert elevator.door == Door.OPEN

    def test_elevator_closes_open_door(self):
        elevator = Elevator(floor=0, top=20, bottom=-2, door=Door.OPEN)

        elevator.move()

        assert elevator.door == Door.SHUT

    def test_elevator_travels_opens_door_at_request_start(self):
        elevator = Elevator(top=20, bottom=-2, floor=-1)

        elevator.request(start = 0, end = 20)
        for _ in range(2):
            elevator.move()

        assert elevator.floor == 0
        assert elevator.door == Door.OPEN

    def test_elevator_travels_opens_door_at_request_end(self):
        elevator = Elevator(top=20, bottom=-2, floor=-1)

        elevator.request(start = 0, end = 20)
        for _ in range(24):
            elevator.move()

        assert elevator.floor == 20
        assert elevator.door == Door.OPEN
