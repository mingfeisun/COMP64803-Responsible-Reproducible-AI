from graph_elements.connections import Connection 
from graph_elements.nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from graph_elements.graph import Graph
from graph_solver.graph_solver import GraphSolver
from graph_elements.graph_generator import GraphGenerator

def main():
    T = 24
    source_solar = Solar('solar1', T, [0, 1])
    source_wind = Wind('wind1', T, [1, 0], offshore=True)
    source_gas = Gas('gas1', T, [1, 1])
    sink = SinkNode('city1', T, [0, 0], 10) 
    graph = Graph(directed=True)
    
    # Adding a node to the graph, nodes are stored as key value pairs, where the
    # key is the node id and the value is the Node object
    graph.add_node(sink)
    graph.add_node(source_solar)
    graph.add_node(source_wind)
    graph.add_node(source_gas)
    # When you add a connection you create a connection object, the method takes 
    # the node id you specified for each node. The connection object contains node_a - source node
    # and node_b - sink node. You also specify a weight which defines the coefficient for the power transmission
    graph.add_connection(source_solar.node_id, sink.node_id, 100000)
    graph.add_connection(source_wind.node_id, sink.node_id, 100000)
    graph.add_connection(source_gas.node_id, sink.node_id, 100000)
    # Calling construct adjacency will iterate all connections to return an adjacency array 
    # the array [i, j] is formatted so [i] is the source, and [j] is the sink
    # this function also returns a node index of key value pairs, where the key is the node id
    # and the index indicates its index in the array
    adjaceny, node_index = graph.construct_adjacency()
    # Any node can be retrieved by calling get node, with the node id, on the graph object 
    node = graph.get_node(list(node_index.keys())[1])
    # nodes also store all their connections as an attribute, if directed connections are only stored
    # as outgoing connections i.e. source nodes store connections but sink nodes generally wont
    id = node.connections[0].node_b.node_id
    
    for node_id, node in graph.nodes.items(): 
        if isinstance(node, SourceNode): 
            power_series = node.get_power_output_series()
            print(node_id, power_series)
        if isinstance(node, SinkNode):
            demand_series = node.demand_profile
            print(node_id, demand_series)
            
    assert len(power_series) == len(demand_series)

    graphgen = GraphGenerator(10, 10, 10, 3, T)
    graph = graphgen.generate_graph()

    solver = GraphSolver(graph, T=T)
    power_allocations, _ = solver.solve()
    #print(f"Power allocations: {power_allocations}")
    
if __name__ == '__main__': 
    main()
