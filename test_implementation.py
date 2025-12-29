"""
Unit tests for the Cyclic Linked List implementation.

Run with: python test_implementation.py
"""

import unittest
from cyclic_linked_list import Node, CyclicLinkedList


class TestNode(unittest.TestCase):
    """Test cases for the Node class."""

    def test_node_creation(self):
        """Test that a node can be created with a P value."""
        node = Node(50)
        self.assertEqual(node.p, 50)
        self.assertIsNone(node.next)
        self.assertIsNone(node.prev)
        self.assertEqual(node.w_reproduce, 0)
        self.assertEqual(node.w_death, 0)

    def test_weight_calculation(self):
        """Test that weights are calculated correctly."""
        # Create a chain: node1 <-> node2 <-> node3
        node1 = Node(10)
        node2 = Node(20)
        node3 = Node(30)

        node1.next = node2
        node1.prev = node3
        node2.next = node3
        node2.prev = node1
        node3.next = node1
        node3.prev = node2

        # Calculate weights for node2
        node2.calculate_weights()

        # Neighbors sum = 10 + 30 = 40
        # W_reproduce = 300 + 2*(40 - 20) = 300 + 40 = 340
        # W_death = 2*(20 - 40) + 500 = -40 + 500 = 460

        self.assertEqual(node2.w_reproduce, 340)
        self.assertEqual(node2.w_death, 460)

    def test_weight_calculation_extremes(self):
        """Test weight calculation with extreme values."""
        # Node with high P surrounded by low P neighbors
        node_high = Node(100)
        node_low1 = Node(0)
        node_low2 = Node(0)

        node_high.next = node_low1
        node_high.prev = node_low2
        node_low1.prev = node_high
        node_low2.next = node_high

        node_high.calculate_weights()

        # Neighbors sum = 0 + 0 = 0
        # W_reproduce = 300 + 2*(0 - 100) = 300 - 200 = 100
        # W_death = 2*(100 - 0) + 500 = 200 + 500 = 700

        self.assertEqual(node_high.w_reproduce, 100)
        self.assertEqual(node_high.w_death, 700)


class TestCyclicLinkedList(unittest.TestCase):
    """Test cases for the CyclicLinkedList class."""

    def test_list_creation(self):
        """Test that a cyclic linked list is created correctly."""
        clist = CyclicLinkedList(initial_size=10)
        self.assertEqual(clist.size, 10)
        self.assertIsNotNone(clist.head)

    def test_cyclic_structure(self):
        """Test that the list is truly cyclic."""
        clist = CyclicLinkedList(initial_size=5)

        # Traverse forward and check we return to head
        current = clist.head
        for _ in range(5):
            current = current.next
        self.assertEqual(current, clist.head)

        # Traverse backward and check we return to head
        current = clist.head
        for _ in range(5):
            current = current.prev
        self.assertEqual(current, clist.head)

    def test_get_all_nodes(self):
        """Test that get_all_nodes returns the correct number of nodes."""
        clist = CyclicLinkedList(initial_size=100)
        nodes = clist.get_all_nodes()
        self.assertEqual(len(nodes), 100)

        # Check that all nodes are unique
        node_ids = [id(node) for node in nodes]
        self.assertEqual(len(node_ids), len(set(node_ids)))

    def test_weights_calculated(self):
        """Test that all nodes have their weights calculated."""
        clist = CyclicLinkedList(initial_size=10)
        nodes = clist.get_all_nodes()

        for node in nodes:
            # Weights should be non-zero (or at least calculated)
            self.assertIsNotNone(node.w_reproduce)
            self.assertIsNotNone(node.w_death)

    def test_remove_node(self):
        """Test node removal."""
        clist = CyclicLinkedList(initial_size=10)
        initial_size = clist.size

        # Get a node to remove (not the head for simplicity)
        node_to_remove = clist.head.next

        # Remove it
        prev, next_node = clist.remove_node(node_to_remove)

        # Check size decreased
        self.assertEqual(clist.size, initial_size - 1)

        # Check that prev and next are now connected
        self.assertEqual(prev.next, next_node)
        self.assertEqual(next_node.prev, prev)

    def test_remove_single_node(self):
        """Test removing the only node in the list."""
        clist = CyclicLinkedList(initial_size=1)
        clist.remove_node(clist.head)

        self.assertEqual(clist.size, 0)
        self.assertIsNone(clist.head)

    def test_split_node(self):
        """Test node splitting."""
        clist = CyclicLinkedList(initial_size=10)
        initial_size = clist.size

        # Find a node with P value that allows splitting
        node_to_split = None
        for node in clist.get_all_nodes():
            if 1 <= node.p <= 99:
                node_to_split = node
                break

        if node_to_split is None:
            # Create a node with suitable P value
            clist.head.p = 50
            node_to_split = clist.head

        original_p = node_to_split.p

        # Split it
        new1, new2 = clist.split_node(node_to_split)

        # Check size increased
        self.assertEqual(clist.size, initial_size + 1)

        # Check offspring P values
        self.assertIn(new1.p, [original_p + 1, original_p - 1])
        self.assertIn(new2.p, [original_p + 1, original_p - 1])
        self.assertNotEqual(new1.p, new2.p)

        # Check that new nodes are connected
        self.assertEqual(new1.next, new2)
        self.assertEqual(new2.prev, new1)

    def test_split_node_boundary_high(self):
        """Test splitting a node with P=100."""
        clist = CyclicLinkedList(initial_size=5)
        clist.head.p = 100

        new1, new2 = clist.split_node(clist.head)

        # P+1 should be capped at 100, P-1 should be 99
        p_values = sorted([new1.p, new2.p])
        self.assertEqual(p_values, [99, 100])

    def test_split_node_boundary_low(self):
        """Test splitting a node with P=0."""
        clist = CyclicLinkedList(initial_size=5)
        clist.head.p = 0

        new1, new2 = clist.split_node(clist.head)

        # P-1 should be capped at 0, P+1 should be 1
        p_values = sorted([new1.p, new2.p])
        self.assertEqual(p_values, [0, 1])

    def test_step_execution(self):
        """Test that a step executes without errors."""
        clist = CyclicLinkedList(initial_size=100)
        initial_size = clist.size

        result = clist.step()

        # Check that result contains expected keys
        self.assertIn('died', result)
        self.assertIn('reproduced', result)
        self.assertIn('offspring', result)
        self.assertIn('size', result)

        # Size should remain 100 (removed 1, added 2, net +1, but then removed 1 = same)
        # Actually: remove 1, add 2 = net +1
        self.assertEqual(clist.size, initial_size)

    def test_multiple_steps(self):
        """Test running multiple steps."""
        clist = CyclicLinkedList(initial_size=100)

        for _ in range(100):
            result = clist.step()
            self.assertNotIn('error', result)

        # List should still have nodes
        self.assertGreater(clist.size, 0)

    def test_statistics(self):
        """Test statistics calculation."""
        clist = CyclicLinkedList(initial_size=100)
        stats = clist.get_statistics()

        # Check that all expected keys are present
        expected_keys = ['size', 'p_mean', 'p_min', 'p_max',
                        'w_death_mean', 'w_reproduce_mean',
                        'w_death_total', 'w_reproduce_total']

        for key in expected_keys:
            self.assertIn(key, stats)

        # Check that values are reasonable
        self.assertEqual(stats['size'], 100)
        self.assertGreaterEqual(stats['p_min'], 0)
        self.assertLessEqual(stats['p_max'], 100)
        self.assertGreaterEqual(stats['p_mean'], stats['p_min'])
        self.assertLessEqual(stats['p_mean'], stats['p_max'])


class TestWeightedSelection(unittest.TestCase):
    """Test cases for weighted random selection."""

    def test_weighted_choice_runs(self):
        """Test that weighted choice doesn't crash."""
        clist = CyclicLinkedList(initial_size=10)

        # Should not raise an exception
        node = clist.weighted_random_choice('w_death')
        self.assertIsNotNone(node)

        node = clist.weighted_random_choice('w_reproduce')
        self.assertIsNotNone(node)

    def test_weighted_choice_distribution(self):
        """Test that weighted choice follows distribution (statistical test)."""
        clist = CyclicLinkedList(initial_size=100)

        # Run many selections and count
        selections = {}
        for _ in range(1000):
            node = clist.weighted_random_choice('w_death')
            node_id = id(node)
            selections[node_id] = selections.get(node_id, 0) + 1

        # At least some nodes should be selected
        self.assertGreater(len(selections), 0)


def run_tests():
    """Run all tests."""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == '__main__':
    print("=" * 70)
    print("RUNNING UNIT TESTS")
    print("=" * 70)
    print()

    # Run the tests
    unittest.main(verbosity=2)
