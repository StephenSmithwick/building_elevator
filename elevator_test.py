from elevator import Door, Elevator, Route

class TestElevator:
    def test_move_opens_door_on_target(self):
        elevator = Elevator(level=0, top=20, bottom=-2, door=Door.SHUT)
        elevator.request(start = 0, end = 1)

        elevator.move()

        assert elevator.door == Door.OPEN

    def test_move_closes_open_door(self):
        elevator = Elevator(level=0, top=20, bottom=-2, door=Door.OPEN)

        elevator.move()

        assert elevator.door == Door.SHUT

    def test_move_opens_door_at_request_start(self):
        elevator = Elevator(top=20, bottom=-2, level=-1)

        elevator.request(start = 0, end = 20)
        for _ in range(2):
            elevator.move()

        assert elevator.level == 0
        assert elevator.door == Door.OPEN

    def test_move_opens_door_at_request_end(self):
        elevator = Elevator(top=20, bottom=-2, level=-1)

        elevator.request(start = 0, end = 20)
        for _ in range(24):
            elevator.move()

        assert elevator.level == 20
        assert elevator.door == Door.OPEN

    def test_request_adds_a_target_for_start_and_end(self):
        elevator = Elevator(level=0, top=20, bottom=-2)

        elevator.request(start = -1, end = 0)

        assert show_plan(elevator) == [[-1, 0]]

    def test_request_interleves_start_if_on_the_way(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = -1, end = 3)

        elevator.request(start = 0, end = 5)

        assert show_plan(elevator) == [[-1, 0, 3, 5]]

    def test_request_interleves_end_if_on_the_way(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = -1, end = 3)
        elevator.request(start = 4, end = 8)

        elevator.request(start = 0, end = 5)

        assert show_plan(elevator) == [[-1, 0, 3, 4, 5, 8]]

    def test_request_dedupes_stops_on_the_way(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = -1, end = 3)

        elevator.request(start = -1, end = 3)

        assert show_plan(elevator) == [[-1, 3]]

    def test_request_internal_to_path_is_added(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = -1, end = 5)

        elevator.request(start = 1, end = 3)

        assert show_plan(elevator) == [[-1, 1, 3, 5]]

    def test_request_continue_from_last_stop(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = 0, end = 5)

        elevator.request(start = 5, end = 0)

        assert show_plan(elevator) == [[0, 5], [5, 0]]

    def test_request_which_must_make_elevator_go_higher_before_turning(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = -1, end = 5)
        elevator.request(start = 5, end = 0)

        elevator.request(start = 6, end = 0)

        assert show_plan(elevator) == [[-1, 5], [6, 5, 0]]

    def test_request_needs_more_than_2_routes(self):
        elevator = Elevator(level=1, top=20, bottom=-2)
        elevator.request(start = -1, end = 5)
        elevator.request(start = 5, end = 0)

        elevator.request(start = 6, end = 0)
        elevator.request(start = 0, end = -3)

        assert show_plan(elevator) == [[-1, 5], [6, 5, 0, -3]]


class TestRoute:
    def test_start_if_ready_down(self):
        route = Route(2, 1)

        route.start_if_ready(1)
        assert route.started == False

        route.start_if_ready(2)
        assert route.started == True

    def test_start_if_ready_up(self):
        route = Route(1, 2)

        route.start_if_ready(2)
        assert route.started == False

        route.start_if_ready(1)
        assert route.started == True

    def test_start_if_ready_is_sticky(self):
        route = Route(1, 2)

        route.start_if_ready(1)
        assert route.started == True

        route.start_if_ready(2)
        assert route.started == True

    def test_mergable_is_true_for_all_requests_in_same_direction(self):
        route = Route(1, 2)
        route.started = False

        assert route.mergable(current_level=1, start=0, end=5) == True

    def test_mergable_is_false_for_requests_before_current_level_if_started(self):
        route = Route(1, 2)
        route.started = True

        assert route.mergable(current_level=1, start=0, end=5) == False

    def test_merge_combines_request_with_route_going_up(self):
        route = Route(1, 3)

        route.merge(2, 4)

        assert route.stops == [1, 2, 3, 4]

    def test_merge_combines_request_with_route_going_down(self):
        route = Route(10, 8)

        route.merge(9, 4)

        assert route.stops == [10, 9, 8, 4]

    def test_merge_removes_duplicate_stops(self):
        route = Route(10, 9)

        route.merge(9, 8)

        assert route.stops == [10, 9, 8]

def show_plan(elevator):
    return [r.stops for r in elevator.routes]
