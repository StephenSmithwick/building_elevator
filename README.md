# Elevator

This Python code is an exercise in implementing the logic to control an Elevator in a few simple Python classes.

## Design Principles
The following principles have guided the requirements documented below
1. Minimize the time passengers spend in the elevator.
2. Minimize the time passengers spend waiting for the elevator.

## Requirements
- An elevator will continue in the same direction once it starts picking up passengers to reduce travel time.
- It will pick up as many passengers as possible along its route to minimize wait times.
- If no passengers have been picked up yet, the elevator can adjust its planned route in any direction.
- Once a passenger’s journey has started, the elevator may adjust its route without going back on itself.
- An elevator will only pick up a passenger when moving in their intended direction.

## Further Improvements
- Create a Command-Line Interface (CLI):
  - Exercising elevator logic conveniently.
  - Validate input parameters.
- Introduce a `Building` class to:
  - Represent number of floors.
  - Support multiple elevators.
  - Simulate elevator movement over time.

## Getting Started
Start by creating a virtual environment and installing the requirements.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running & Testing the Elevator class

To run all tests
```bash
pytest
```

To run a specific test
```bash
pytest -k [test name]
```


## Linting

For consistent formatting:
```bash
ruff check
```
