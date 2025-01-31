"""
connections.py
==============

This module contains functionality for managing the connections between two 
`Node` objects in an energy network. Each `Connection` represents an edge 
with a specified power capacity and a calculated efficiency factor based on 
distance and converter losses.

Examples
--------
>>> from connections import Connection
>>> from nodes import Node
>>> n1 = Node("N1", 24, (0, 0))
>>> n2 = Node("N2", 24, (1000, 1000))
>>> conn = Connection(n1, n2, power_capacity=500.0)
>>> efficiency_weight = conn.transmission_loss_weight()
>>> print(efficiency_weight)
0.98  # Example output
"""

from typing import Callable
import numpy as np
from graph_elements.nodes import Node, SourceNode, SinkNode
from scipy.spatial.distance import euclidean

class Connection:
    """
    A connection (edge) between two nodes in a graph.

    This class models a unidirectional or bidirectional link (depending on graph 
    context) between `node_a` and `node_b`. It includes attributes for power capacity, 
    the current power flowing through the connection, and a calculated weight that 
    represents transmission efficiency (based on distance and converter losses).

    Parameters
    ----------
    node_a : Node
        The source or first node.
    node_b : Node
        The destination or second node.
    power_capacity : float
        The maximum power capacity (in MW, kW, etc. as determined by the system context) 
        for this connection.

    Attributes
    ----------
    node_a : Node
        The source or first node of this connection.
    node_b : Node
        The destination or second node of this connection.
    power_capacity : float
        Power capacity limit for this connection.
    power : float
        Current power (in the same units as `power_capacity`) being channeled 
        by the connection.
    weight : float
        Represents the efficiency of power transfer (0 to 1). Computed via 
        `transmission_loss_weight()`.

    Notes
    -----
    The `weight` attribute is used to represent an overall efficiency factor for 
    electricity transfer. A value of 1 means no losses; a value of 0 means 
    complete loss or inability to transfer power. Realistically, it is expected 
    to be in the range (0.8 - 1.0) for most practical connections, but can be 
    lower for very long distances.
    """

    def __init__(self, node_a: Node, node_b: Node, power_capacity: float):
        """
        Initialize a Connection instance.

        Parameters
        ----------
        node_a : Node
            The source or first node.
        node_b : Node
            The destination or second node.
        power_capacity : float
            The power capacity limit for this connection.
        """
        self.node_a = node_a
        self.node_b = node_b
        self.power_capacity = power_capacity
        self.power = 0.0

        # Compute efficiency (weight) based on the nodes' distance and 
        # converter losses.
        self.weight = self.transmission_loss_weight()

    def transmission_loss_weight(self) -> float:
        """
        Compute the efficiency factor based on power transmission losses.

        This method calculates the overall efficiency by:
          1. Determining the distance-based loss (1% per 100 km).
          2. Selecting a random converter efficiency at the source 
             between 99.2% and 99.3%.
          3. Multiplying the distance loss factor by the converter 
             efficiency to yield a final efficiency value.

        Returns
        -------
        float
            The efficiency factor in the range [0, 1], where 1 means 
            no losses and 0 means complete loss (though practically 
            values should remain close to 1 for moderate distances).

        References
        ----------
        https://www.nationalgrid.com/sites/default/files/documents/13784-High%20Voltage%20Direct%20Current%20Electricity%20%E2%80%93%20technical%20information.pdf

        Examples
        --------
        >>> from nodes import Node
        >>> n1 = Node("N1", 24, (0, 0))
        >>> n2 = Node("N2", 24, (100000, 0))  # 100 km away
        >>> conn = Connection(n1, n2, power_capacity=1000)
        >>> conn.weight  # Approximately 0.99 * random converter efficiency
        0.98019
        """
        # Calculate the Euclidean distance between node coordinates
        distance = euclidean(
            np.array(self.node_a.cartesian_coordinates),
            np.array(self.node_b.cartesian_coordinates)
        )
        # Convert distance-based loss: 1% per 100 km
        distance_loss_factor = 1 - (0.01 * (distance / 100_000))

        # Random converter efficiency (range: 99.2% to 99.3%)
        converter_efficiency = np.random.uniform(0.992, 0.993)

        # Multiply converter efficiency by distance-based efficiency
        total_efficiency = converter_efficiency * distance_loss_factor

        # Ensure the result is not negative
        return max(total_efficiency, 0)
