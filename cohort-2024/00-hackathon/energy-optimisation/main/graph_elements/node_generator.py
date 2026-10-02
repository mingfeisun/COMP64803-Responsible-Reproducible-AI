import random
import numpy as np
from graph_elements.connections import Connection
from graph_elements.nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from graph_elements.graph import Graph

# Define UK-like coordinate bounds (scaled in km)
MIN_X, MAX_X = 0, 600
MIN_Y, MAX_Y = 0, 1000

def generate_nodes(graph, num_solar, num_wind, num_gas, num_sinks, time_range):
    """
    Generates and adds nodes to the graph. Each source is connected to every sink.

    Parameters:
    ----------
    graph : Graph
        The graph instance to add nodes and connections to.
    num_solar : int
        Number of solar power nodes.
    num_wind : int
        Number of wind power nodes.
    num_gas : int
        Number of gas power nodes.
    num_sinks : int
        Number of sink nodes.
    time_range : int
        The time range for power simulations.
    """
    source_nodes = []
    sink_nodes = []
    node_id = 0

    # Create sources (Solar, Wind, Gas)
    for _ in range(num_solar):
        node = Solar(f"solar{node_id}", time_range, [random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_Y)])
        source_nodes.append(node)
        graph.add_node(node)
        node_id += 1

    for _ in range(num_wind):
        offshore = random.choice([True, False])
        node = Wind(f"wind{node_id}", time_range, [random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_Y)], offshore)
        source_nodes.append(node)
        graph.add_node(node)
        node_id += 1

    for _ in range(num_gas):
        node = Gas(f"gas{node_id}", time_range, [random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_Y)])
        source_nodes.append(node)
        graph.add_node(node)
        node_id += 1

    # Create sink nodes
    for _ in range(num_sinks):
        econ_coefficient = random.uniform(0.1, 1.0)
        node = SinkNode(f"sink{node_id}", time_range, [random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y, MAX_Y)], econ_coefficient)
        sink_nodes.append(node)
        graph.add_node(node)
        node_id += 1

    # Connect every source to every sink
    for source in source_nodes:
        for sink in sink_nodes:
            distance = np.linalg.norm(np.array(source.cartesian_coordinates) - np.array(sink.cartesian_coordinates))
            power_capacity = max(50_000, 1 / distance)  # Ensure a reasonable power capacity
            graph.add_connection(source.node_id, sink.node_id, power_capacity)

    return source_nodes, sink_nodes
