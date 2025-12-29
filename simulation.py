"""
Simulation script for the Cyclic Linked List with Death and Reproduction Mechanics

This script demonstrates the usage of the CyclicLinkedList class and runs
a simulation showing how the population evolves over time.
"""

from cyclic_linked_list import CyclicLinkedList
import matplotlib.pyplot as plt
import numpy as np


def run_simulation(steps=1000, initial_size=100, verbose=False):
    """
    Run a simulation of the cyclic linked list evolution.

    Args:
        steps: Number of death-reproduction cycles to execute
        initial_size: Initial number of nodes
        verbose: If True, print detailed information for each step

    Returns:
        Dictionary with simulation history
    """
    # Initialize the cyclic linked list
    clist = CyclicLinkedList(initial_size=initial_size)

    # Track history
    history = {
        'step': [],
        'size': [],
        'p_mean': [],
        'p_min': [],
        'p_max': [],
        'died': [],
        'reproduced': []
    }

    print(f"Initial state: {clist}")
    print(f"Initial statistics: {clist.get_statistics()}\n")

    # Run simulation
    for step in range(steps):
        result = clist.step()

        if 'error' in result:
            print(f"Simulation stopped at step {step}: {result['error']}")
            break

        # Record history
        stats = clist.get_statistics()
        history['step'].append(step)
        history['size'].append(stats['size'])
        history['p_mean'].append(stats['p_mean'])
        history['p_min'].append(stats['p_min'])
        history['p_max'].append(stats['p_max'])
        history['died'].append(result['died'])
        history['reproduced'].append(result['reproduced'])

        if verbose and step % 100 == 0:
            print(f"Step {step}: {clist}")
            print(f"  Died: P={result['died']}, Reproduced: P={result['reproduced']} -> {result['offspring']}")

    print(f"\nFinal state after {steps} steps: {clist}")
    print(f"Final statistics: {clist.get_statistics()}")

    return history


def plot_simulation_results(history):
    """
    Plot the simulation results.

    Args:
        history: Dictionary with simulation history from run_simulation()
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: Population size over time
    axes[0, 0].plot(history['step'], history['size'], 'b-', linewidth=1)
    axes[0, 0].set_xlabel('Step')
    axes[0, 0].set_ylabel('Population Size')
    axes[0, 0].set_title('Population Size Over Time')
    axes[0, 0].grid(True, alpha=0.3)

    # Plot 2: Mean P value over time
    axes[0, 1].plot(history['step'], history['p_mean'], 'g-', linewidth=1)
    axes[0, 1].set_xlabel('Step')
    axes[0, 1].set_ylabel('Mean P Value')
    axes[0, 1].set_title('Mean P Value Over Time')
    axes[0, 1].grid(True, alpha=0.3)

    # Plot 3: P value range over time
    axes[1, 0].fill_between(history['step'], history['p_min'], history['p_max'], alpha=0.3)
    axes[1, 0].plot(history['step'], history['p_mean'], 'r-', linewidth=2, label='Mean')
    axes[1, 0].set_xlabel('Step')
    axes[1, 0].set_ylabel('P Value')
    axes[1, 0].set_title('P Value Range Over Time (Min, Mean, Max)')
    axes[1, 0].legend()
    axes[1, 0].grid(True, alpha=0.3)

    # Plot 4: Distribution of P values that died vs reproduced
    axes[1, 1].hist(history['died'], bins=30, alpha=0.5, label='Died', color='red')
    axes[1, 1].hist(history['reproduced'], bins=30, alpha=0.5, label='Reproduced', color='green')
    axes[1, 1].set_xlabel('P Value')
    axes[1, 1].set_ylabel('Frequency')
    axes[1, 1].set_title('Distribution of P Values: Death vs Reproduction')
    axes[1, 1].legend()
    axes[1, 1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('simulation_results.png', dpi=150)
    print("\nPlot saved as 'simulation_results.png'")
    plt.show()


def demonstrate_single_step():
    """Demonstrate a single step of the simulation with detailed output."""
    print("=" * 70)
    print("DEMONSTRATION OF A SINGLE STEP")
    print("=" * 70)

    # Create a small list for demonstration
    clist = CyclicLinkedList(initial_size=10)

    print("\nInitial nodes:")
    for i, node in enumerate(clist.get_all_nodes()):
        print(f"  Node {i}: {node}")

    print("\nExecuting one step...")
    result = clist.step()

    print(f"\nStep result:")
    print(f"  Node died: P={result['died']}")
    print(f"  Node reproduced: P={result['reproduced']}")
    print(f"  Offspring: P={result['offspring'][0]} and P={result['offspring'][1]}")
    print(f"  New size: {result['size']}")

    print("\nNodes after step:")
    for i, node in enumerate(clist.get_all_nodes()):
        print(f"  Node {i}: {node}")

    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Demonstrate a single step
    demonstrate_single_step()

    print("\n\n")

    # Run a longer simulation
    print("=" * 70)
    print("RUNNING FULL SIMULATION")
    print("=" * 70)

    history = run_simulation(steps=1000, initial_size=100, verbose=True)

    # Plot results (requires matplotlib)
    try:
        plot_simulation_results(history)
    except ImportError:
        print("\nMatplotlib not available. Skipping plots.")
    except Exception as e:
        print(f"\nError creating plots: {e}")
