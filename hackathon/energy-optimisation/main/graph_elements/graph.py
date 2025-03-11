"""
graph.py
========

This module provides the Graph class for constructing and managing
directed or undirected graphs of Node objects and their Connections.

Examples
--------
>>> from graph import Graph
>>> from nodes import Node
>>>
>>> # Create a simple graph
>>> g = Graph(directed=False)
>>> n1 = Node(node_id="A", time_range=24, cartesian_coordinates=(0, 0))
>>> n2 = Node(node_id="B", time_range=24, cartesian_coordinates=(1, 1))
>>> g.add_node(n1)
>>> g.add_node(n2)
>>> g.add_connection("A", "B", power_capacity=100)
>>> adj_matrix, index_map = g.construct_adjacency()
>>> print(adj_matrix)
"""

import numpy as np
from .nodes import SinkNode, SourceNode, Node
from .connections import Connection


class Graph:
    """
    A directed or undirected graph of nodes and connections.

    This class stores nodes (in a dictionary) and the connections (in a list).
    It provides methods to add nodes, add connections, and build an adjacency
    matrix for various graph operations.

    Parameters
    ----------
    directed : bool, optional
        If True, construct a directed graph; otherwise undirected.
        Defaults to False.

    Attributes
    ----------
    nodes : dict of str -> Node
        A dictionary of node objects, keyed by their node_id.
    connections : list of Connection
        A list of Connection objects between nodes.
    directed : bool
        Indicates whether the graph is directed (True) or undirected (False).
    """

    def __init__(self, directed: bool = False):
        """
        Initialize the graph with optional directionality.

        Parameters
        ----------
        directed : bool, optional
            Set to True for a directed graph; False for undirected.
            Default is False.
        """
        self.nodes = {}
        self.connections = []
        self.directed = directed

    def add_node(self, node: Node):
        """
        Add a single node to the graph.

        Parameters
        ----------
        node : Node
            The node object to be added.

        Returns
        -------
        None
        """
        self.nodes[node.node_id] = node

    def add_nodes(self, nodes: list[Node]):
        """
        Add multiple nodes to the graph.

        Parameters
        ----------
        nodes : list of Node
            A list of node objects to be added.

        Returns
        -------
        None
        """
        for node in nodes:
            self.nodes[node.node_id] = node

    def get_sinks(self):
        """
        Retrieve all sink nodes from the graph.

        A sink node is identified by being an instance of `SinkNode`.

        Returns
        -------
        list of SinkNode
            A list containing all sink nodes in the graph.
        """
        sink_nodes = []
        for node in self.nodes.values():
            if isinstance(node, SinkNode):
                sink_nodes.append(node)
        return sink_nodes

    def get_sources(self):
        """
        Retrieve all source nodes from the graph.

        A source node is identified by being an instance of `SourceNode`.

        Returns
        -------
        list of SourceNode
            A list containing all source nodes in the graph.
        """
        source_nodes = []
        for node in self.nodes.values():
            if isinstance(node, SourceNode):
                source_nodes.append(node)
        return source_nodes

    def add_connection(self, node_a_id: str, node_b_id: str, power_capacity: float):
        """
        Add a connection between two existing nodes in the graph.

        Parameters
        ----------
        node_a_id : str
            The source node's ID.
        node_b_id : str
            The destination node's ID.
        power_capacity : float
            The power capacity (or "weight") of the connection.

        Raises
        ------
        ValueError
            If either node_a_id or node_b_id is not found in the graph.

        Returns
        -------
        None
        """
        if node_a_id not in self.nodes or node_b_id not in self.nodes:
            raise ValueError("Node not found in the graph.")
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]

        connection = Connection(node_a, node_b, power_capacity)
        self.connections.append(connection)

        # Update adjacency in each node
        node_a.set_connection(connection, node_b_id)

        if not self.directed:
            # In undirected graphs, record the connection on node_b as well
            node_b.set_connection(connection, node_a_id)

    def get_node(self, node_id: str) -> Node:
        """
        Retrieve a node object by its ID.

        Parameters
        ----------
        node_id : str
            The ID of the node to retrieve.

        Returns
        -------
        Node or None
            The node object if found, otherwise None.
        """
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str) -> list[Connection]:
        """
        Retrieve all connections for a given node.

        Parameters
        ----------
        node_id : str
            The ID of the node whose neighbors to retrieve.

        Returns
        -------
        list of Connection
            A list of connections originating from or associated with
            the specified node.

        Raises
        ------
        KeyError
            If the node_id does not exist in the graph.
        """
        node = self.nodes[node_id]  # Raises KeyError if missing
        return node.connections

    def construct_adjacency(self):
        """
        Construct an adjacency matrix representing the graph.

        For each connection, the matrix entry [i, j] is set to the
        `power_capacity` of the connection. In a directed graph,
        entry [i, j] will be nonzero if there is a connection from i to j.
        In an undirected graph, both [i, j] and [j, i] are set to this value.

        Returns
        -------
        adjacency_matrix : np.ndarray
            A 2D NumPy array where rows and columns are indexed by nodes.
        node_index : dict of str -> int
            A mapping from node IDs to their row/column index in the matrix.
        """
        n = len(self.nodes)
        adjacency_matrix = np.zeros((n, n))

        # Create an index mapping for node_id -> matrix index
        node_index = {node_id: i for i, node_id in enumerate(self.nodes.keys())}

        for connection in self.connections:
            w = connection.weight
            a_id = connection.node_a.node_id
            b_id = connection.node_b.node_id
            i, j = node_index[a_id], node_index[b_id]

            if self.directed:
                # Optionally, you could further customize how directed edges work
                adjacency_matrix[i, j] = w
            else:
                adjacency_matrix[i, j] = w
                adjacency_matrix[j, i] = w

        return adjacency_matrix, node_index
