"""
Cyclic Linked List Implementation with Death and Reproduction Mechanics

This module implements a cyclic linked list where each node has:
- P: an integer value from 0 to 100
- W_reproduce: reproduction weight = 300 + 2*(sum of neighbors' P - P)
- W_death: death weight = 2*(P - sum of neighbors' P) + 500

The simulation includes death and reproduction procedures based on weighted random selection.
"""

import random


class Node:
    """A node in the cyclic linked list."""

    def __init__(self, p_value):
        """
        Initialize a node with a P value.

        Args:
            p_value: Integer value from 0 to 100
        """
        self.p = p_value
        self.next = None
        self.prev = None
        self.w_reproduce = 0
        self.w_death = 0

    def calculate_weights(self):
        """
        Calculate W_reproduce and W_death based on neighbors' P values.

        W_reproduce = 300 + 2*(sum of neighbors' P - P)
        W_death = 2*(P - sum of neighbors' P) + 500
        """
        if self.next is None or self.prev is None:
            return

        neighbors_sum = self.prev.p + self.next.p
        self.w_reproduce = 300 + 2 * (neighbors_sum - self.p)
        self.w_death = 2 * (self.p - neighbors_sum) + 500

    def __repr__(self):
        return f"Node(P={self.p}, W_r={self.w_reproduce}, W_d={self.w_death})"


class CyclicLinkedList:
    """A cyclic linked list with death and reproduction mechanics."""

    def __init__(self, initial_size=100, p_range=(0, 100)):
        """
        Initialize a cyclic linked list.

        Args:
            initial_size: Number of nodes to create (default: 100)
            p_range: Tuple of (min, max) for P values (default: (0, 100))
        """
        self.head = None
        self.size = 0

        # Create initial nodes
        for _ in range(initial_size):
            p_value = random.randint(p_range[0], p_range[1])
            self.append(p_value)

        # Calculate initial weights
        self.recalculate_all_weights()

    def append(self, p_value):
        """Add a node with the given P value to the list."""
        new_node = Node(p_value)

        if self.head is None:
            # First node - points to itself
            self.head = new_node
            new_node.next = new_node
            new_node.prev = new_node
        else:
            # Insert at the end (before head)
            tail = self.head.prev
            tail.next = new_node
            new_node.prev = tail
            new_node.next = self.head
            self.head.prev = new_node

        self.size += 1

    def recalculate_all_weights(self):
        """Recalculate weights for all nodes in the list."""
        if self.head is None:
            return

        current = self.head
        for _ in range(self.size):
            current.calculate_weights()
            current = current.next

    def get_all_nodes(self):
        """Return a list of all nodes in the cyclic linked list."""
        if self.head is None:
            return []

        nodes = []
        current = self.head
        for _ in range(self.size):
            nodes.append(current)
            current = current.next

        return nodes

    def weighted_random_choice(self, weight_attr):
        """
        Choose a random node based on weights.

        Args:
            weight_attr: The attribute name for weights ('w_death' or 'w_reproduce')

        Returns:
            Selected node
        """
        nodes = self.get_all_nodes()
        weights = [getattr(node, weight_attr) for node in nodes]

        # Handle edge case where all weights are non-positive
        if all(w <= 0 for w in weights):
            # If all weights are non-positive, make them all equal
            weights = [1] * len(weights)

        return random.choices(nodes, weights=weights, k=1)[0]

    def remove_node(self, node):
        """
        Remove a node from the list and stitch together its neighbors.

        Args:
            node: The node to remove

        Returns:
            Tuple of (prev_node, next_node) - the former neighbors
        """
        if self.size == 0:
            return None, None

        if self.size == 1:
            self.head = None
            self.size = 0
            return None, None

        prev_node = node.prev
        next_node = node.next

        # Stitch together neighbors
        prev_node.next = next_node
        next_node.prev = prev_node

        # Update head if necessary
        if node == self.head:
            self.head = next_node

        self.size -= 1
        return prev_node, next_node

    def split_node(self, node):
        """
        Split a node into two nodes with P+1 and P-1.

        Args:
            node: The node to split

        Returns:
            Tuple of (new_node1, new_node2) - the two new nodes
        """
        # Create two new nodes with P+1 and P-1
        p_plus = min(node.p + 1, 100)  # Cap at 100
        p_minus = max(node.p - 1, 0)   # Floor at 0

        new_node1 = Node(p_plus)
        new_node2 = Node(p_minus)

        # Insert the two new nodes in place of the original node
        prev_node = node.prev
        next_node = node.next

        # Connect: prev -> new_node1 -> new_node2 -> next
        prev_node.next = new_node1
        new_node1.prev = prev_node
        new_node1.next = new_node2
        new_node2.prev = new_node1
        new_node2.next = next_node
        next_node.prev = new_node2

        # Update head if necessary
        if node == self.head:
            self.head = new_node1

        self.size += 1  # Net increase of 1 node (removed 1, added 2)

        return new_node1, new_node2

    def step(self):
        """
        Execute one step of the death-reproduction cycle:
        1. Choose a node weighted by W_death and remove it
        2. Recalculate weights for affected neighbors
        3. Choose a node weighted by W_reproduce and split it
        4. Recalculate weights for affected nodes

        Returns:
            Dictionary with information about the step
        """
        if self.size < 2:
            return {"error": "Not enough nodes to perform step"}

        # Step 1: Choose and remove a node (death)
        dying_node = self.weighted_random_choice('w_death')
        dying_p = dying_node.p
        prev_neighbor, next_neighbor = self.remove_node(dying_node)

        # Step 2: Recalculate weights for the stitched neighbors
        if prev_neighbor:
            prev_neighbor.calculate_weights()
        if next_neighbor and next_neighbor != prev_neighbor:
            next_neighbor.calculate_weights()

        # Step 3: Choose and split a node (reproduction)
        reproducing_node = self.weighted_random_choice('w_reproduce')
        reproducing_p = reproducing_node.p
        new_node1, new_node2 = self.split_node(reproducing_node)

        # Step 4: Recalculate weights for affected nodes
        # The new nodes and their neighbors need recalculation
        new_node1.calculate_weights()
        new_node2.calculate_weights()
        if new_node1.prev:
            new_node1.prev.calculate_weights()
        if new_node2.next:
            new_node2.next.calculate_weights()

        return {
            "died": dying_p,
            "reproduced": reproducing_p,
            "offspring": (new_node1.p, new_node2.p),
            "size": self.size
        }

    def get_statistics(self):
        """Get statistics about the current state of the list."""
        nodes = self.get_all_nodes()
        if not nodes:
            return {}

        p_values = [node.p for node in nodes]
        w_deaths = [node.w_death for node in nodes]
        w_reproduces = [node.w_reproduce for node in nodes]

        return {
            "size": self.size,
            "p_mean": sum(p_values) / len(p_values),
            "p_min": min(p_values),
            "p_max": max(p_values),
            "w_death_mean": sum(w_deaths) / len(w_deaths),
            "w_reproduce_mean": sum(w_reproduces) / len(w_reproduces),
            "w_death_total": sum(w_deaths),
            "w_reproduce_total": sum(w_reproduces)
        }

    def __repr__(self):
        stats = self.get_statistics()
        return f"CyclicLinkedList(size={stats.get('size', 0)}, P_mean={stats.get('p_mean', 0):.2f})"
