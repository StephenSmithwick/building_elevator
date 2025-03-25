There are many elevator models currently available.  For this repo I will suppose an elevator with
system with floor request buttons on the floor which should allow for more interesting optimization
of elevator logic.

# Requirements
Given `n` elevators and `m` floors
1. A user on floor i will be able to request any other floor calling for an elevator.

# Running the code
## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Tests

```
pytest
```


## Linting

```
ruff check
```
