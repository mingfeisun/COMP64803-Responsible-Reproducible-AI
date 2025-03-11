import numpy as np
import random
from graph_elements.graph import Graph
from graph_elements.nodes import Solar, Wind, Gas, SinkNode

class GraphGenerator:
    """
    Generates a random directed acyclic graph (DAG) with sources (Solar, Wind, Gas) and sinks.

    Parameters
    ----------
    num_solar : int
        Number of solar power nodes.
    num_wind : int
        Number of wind power nodes.
    num_gas : int
        Number of gas power nodes.
    num_sinks : int
        Number of sink nodes.
    time_range : int
        Time range for power simulations.

    Methods
    -------
    generate_graph()
        Generates the random DAG and returns a `Graph` object.
    """

    def __init__(self, num_solar, num_wind, num_gas, num_sinks, time_range):
        self.num_solar = num_solar
        self.num_wind = num_wind
        self.num_gas = num_gas
        self.num_sinks = num_sinks
        self.time_range = time_range

        self.total_sources = num_solar + num_wind + num_gas
        self.total_nodes = self.total_sources + num_sinks
        self.positions = {}  # Stores Cartesian coordinates of each node
        self.nodes = []  # Stores node objects
        self.graph = Graph(directed=True)  # Create an empty directed graph

        # UK bounding box (approximate, scaled in km)
        self.min_x, self.max_x = 0, 600
        self.min_y, self.max_y = 0, 1000

    def _generate_positions(self):
        """Randomly assigns positions within a UK-scale bounding box."""
        for i in range(self.total_nodes):
            self.positions[f"N{i}"] = (
                random.uniform(self.min_x, self.max_x),
                random.uniform(self.min_y, self.max_y),
            )

    def _create_nodes(self):
        """Creates source and sink nodes with random attributes."""
        node_id = 0

        # Add solar nodes
        for _ in range(self.num_solar):
            node = Solar(f"N{node_id}", self.time_range, self.positions[f"N{node_id}"])
            self.nodes.append(node)
            self.graph.add_node(node)
            node_id += 1

        # Add wind nodes
        for _ in range(self.num_wind):
            offshore = random.choice([True, False])  # Randomly set onshore/offshore
            node = Wind(f"N{node_id}", self.time_range, self.positions[f"N{node_id}"], offshore)
            self.nodes.append(node)
            self.graph.add_node(node)
            node_id += 1

        # Add gas nodes
        for _ in range(self.num_gas):
            node = Gas(f"N{node_id}", self.time_range, self.positions[f"N{node_id}"])
            self.nodes.append(node)
            self.graph.add_node(node)
            node_id += 1

        # Add sink nodes
        for _ in range(self.num_sinks):
            econ_coefficient = random.uniform(0.1, 1.0)  # Arbitrary economic penalty
            node = SinkNode(f"N{node_id}", self.time_range, self.positions[f"N{node_id}"], econ_coefficient)
            self.nodes.append(node)
            self.graph.add_node(node)
            node_id += 1

    def _connect_nodes(self):
        """Ensures every source node is connected to every sink node with no direct sink-to-sink or source-to-source connections."""
        source_nodes = [node for node in self.nodes if isinstance(node, (Solar, Wind, Gas))]
        sink_nodes = [node for node in self.nodes if isinstance(node, SinkNode)]

        for source in source_nodes:
            for sink in sink_nodes:
                distance = np.linalg.norm(
                    np.array(self.positions[source.node_id]) - np.array(self.positions[sink.node_id])
                )
                self.graph.add_connection(source.node_id, sink.node_id, 1 / distance)  # Inverse distance as weight


    def generate_graph(self):
        """Generates a graph with nodes and edges."""
        self._generate_positions()
        self._create_nodes()
        self._connect_nodes()
        return self.graph
