# Cyclic Linked List with Death and Reproduction Mechanics

A Python implementation of a cyclic (circular) linked list with evolutionary dynamics based on weighted death and reproduction mechanisms.

## Overview

This project implements a cyclic linked list of 100 nodes where each node:
- Has an integer value **P** ranging from 0 to 100
- Calculates a **reproduction weight** (W_reproduce) based on its neighbors
- Calculates a **death weight** (W_death) based on its neighbors
- Participates in an evolutionary cycle of death and reproduction

## Mathematical Model

### Node Weights

Each node calculates two weights based on its value P and its neighbors' values:

- **W_reproduce** = 300 + 2 × (sum of neighbors' P - P)
- **W_death** = 2 × (P - sum of neighbors' P) + 500

### Evolutionary Cycle

Each simulation step consists of:

1. **Death Phase**:
   - Randomly select a node with probability proportional to W_death
   - Remove the node from the list
   - Stitch together its former neighbors
   - Recalculate weights for affected neighbors

2. **Reproduction Phase**:
   - Randomly select a node with probability proportional to W_reproduce
   - Split the node into two new nodes with values P+1 and P-1
   - Recalculate weights for affected nodes

## Project Structure

```
.
├── cyclic_linked_list.py   # Core implementation (Node and CyclicLinkedList classes)
├── simulation.py            # Simulation runner and visualization
├── test_implementation.py   # Unit tests
└── README.md               # This file
```

## Classes

### Node

Represents a single node in the cyclic linked list.

**Attributes**:
- `p`: Integer value (0-100)
- `next`: Reference to next node
- `prev`: Reference to previous node
- `w_reproduce`: Reproduction weight
- `w_death`: Death weight

**Methods**:
- `calculate_weights()`: Computes W_reproduce and W_death based on neighbors

### CyclicLinkedList

Manages the cyclic linked list and evolutionary dynamics.

**Methods**:
- `__init__(initial_size=100)`: Create a list with random P values
- `step()`: Execute one death-reproduction cycle
- `get_statistics()`: Get current population statistics
- `weighted_random_choice(weight_attr)`: Select node based on weights
- `remove_node(node)`: Remove a node and stitch neighbors
- `split_node(node)`: Split a node into two offspring

## Usage

### Basic Usage

```python
from cyclic_linked_list import CyclicLinkedList

# Create a cyclic linked list with 100 nodes
clist = CyclicLinkedList(initial_size=100)

# Get current statistics
stats = clist.get_statistics()
print(f"Population size: {stats['size']}")
print(f"Mean P value: {stats['p_mean']:.2f}")

# Execute one evolutionary step
result = clist.step()
print(f"Died: P={result['died']}")
print(f"Reproduced: P={result['reproduced']} -> offspring {result['offspring']}")
```

### Running a Simulation

```python
from simulation import run_simulation, plot_simulation_results

# Run 1000 steps
history = run_simulation(steps=1000, initial_size=100, verbose=True)

# Plot the results
plot_simulation_results(history)
```

### Command Line

```bash
# Run the simulation
python simulation.py

# Run tests
python test_implementation.py
```

## Example Output

```
Initial state: CyclicLinkedList(size=100, P_mean=49.23)

Step 0: CyclicLinkedList(size=100, P_mean=49.31)
  Died: P=75, Reproduced: P=42 -> (43, 41)

Step 100: CyclicLinkedList(size=100, P_mean=50.12)
  Died: P=62, Reproduced: P=38 -> (39, 37)

Final state after 1000 steps: CyclicLinkedList(size=100, P_mean=49.87)
```

## Key Features

- **Weighted Selection**: Both death and reproduction use weighted random selection
- **Dynamic Weights**: Weights are recalculated after each modification
- **Boundary Handling**: P values are capped at 0 and 100
- **Efficient Updates**: Only affected nodes recalculate weights
- **Statistics Tracking**: Built-in methods for monitoring population dynamics

## Dependencies

- Python 3.6+
- matplotlib (optional, for visualization)
- numpy (optional, for plotting)

## Installation

```bash
# No installation needed - just copy the files

# Optional: Install visualization dependencies
pip install matplotlib numpy
```

## Testing

Run the test suite to verify correctness:

```bash
python test_implementation.py
```

## Implementation Details

### Cyclic Structure

The list maintains a circular structure where:
- The last node's `next` points to the first node
- The first node's `prev` points to the last node
- This ensures every node always has exactly two neighbors

### Weight Calculation

Weights favor:
- **High death probability**: Nodes with P values much higher than neighbors
- **High reproduction probability**: Nodes with P values much lower than neighbors

This creates an evolutionary pressure toward local equilibrium.

### Thread Safety

This implementation is **not thread-safe**. For concurrent usage, add appropriate locking mechanisms.

## License

This project is provided as-is for educational and research purposes.
