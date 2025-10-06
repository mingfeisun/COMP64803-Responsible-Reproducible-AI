from flask import Flask, render_template, url_for
import json
from graph_elements.connections import Connection
from graph_elements.nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from graph_elements.graph import Graph

app = Flask(__name__)

T = 5
source_solar = Solar('solar1', T, [0, 1])
source_wind = Wind('wind1', T, [1, 0], offshore=True)
source_gas = Gas('gas1', T, [1, 1])
sink = SinkNode('city1', T, [0, 0], 10) 
graph = Graph(directed=True)

graph.add_node(sink)
graph.add_node(source_solar)
graph.add_node(source_wind)
graph.add_node(source_gas)
graph.add_connection(source_solar.node_id, sink.node_id, 100000)
graph.add_connection(source_wind.node_id, sink.node_id, 100000)
graph.add_connection(source_gas.node_id, sink.node_id, 100000)

@app.route("/")
def index():
    data = {"nodes": [], "links": []}

    for name, node in graph.nodes.items():
        image_url = url_for("static", filename="unknown.jpg")
        if isinstance(node, Solar):
            image_url = url_for("static", filename="solar.jpg")
        elif isinstance(node, Wind):
            image_url = url_for("static", filename="wind.webp")
        elif isinstance(node, Gas):
            image_url = url_for("static", filename="gas.webp")
        elif isinstance(node, SinkNode):
            image_url = url_for("static", filename="city.webp")

        data["nodes"].append({
            "id": name,
            "type": "source" if isinstance(node, SourceNode) else "sink",
            "image": image_url
        })

    for connection in graph.connections:
        data["links"].append({
            "source": connection.node_a.node_id,
            "target": connection.node_b.node_id,
            "power": connection.weight*100
        })

    return render_template("index.html", graph_data=json.dumps(data))

if __name__ == "__main__":
    app.run(debug=True)
