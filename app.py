import sys, os
sys.path.append(os.path.dirname(__file__))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

from converter import (
    parse_edge_list,
    to_cytoscape,
    edges_to_adj_list,
    edges_to_adj_matrix
)

from graph_algorithms import (
    bfs, dfs, dijkstra,
    prim_mst, kruskal_mst,
    ford_fulkerson,
    is_bipartite,
    fleury_algorithm,
    hierholzer_algorithm
)

app = Flask(__name__)
CORS(app)

GRAPH_STORE = {"edges": []}

@app.route("/")
def index():
    return render_template("index.html")

# ================= GRAPH =================

@app.route("/api/convert", methods=["POST"])
def api_convert():
    data = request.get_json()
    edges = parse_edge_list(data.get("edge_text", ""))
    GRAPH_STORE["edges"] = edges

    nodes = sorted({u for u,v,w in edges} | {v for u,v,w in edges})
    return jsonify({
        "cytoscape": {
            "elements": to_cytoscape(nodes, edges)
        }
    })

@app.route("/api/save", methods=["GET"])
def save_graph():
    return jsonify(GRAPH_STORE)

@app.route("/api/load", methods=["POST"])
def load_graph():
    data = request.get_json()
    GRAPH_STORE["edges"] = data.get("edges", [])
    return jsonify({"status": "ok"})

# ================= ALGORITHMS =================

@app.route("/api/algorithm/<algo>", methods=["POST"])
def api_algorithm(algo):
    data = request.get_json()
    edges = parse_edge_list(data.get("edge_text", ""))
    start = data.get("start")
    target = data.get("target")

    if algo == "bfs":
        return jsonify(bfs(edges, start))
    if algo == "dfs":
        return jsonify(dfs(edges, start))
    if algo == "dijkstra":
        return jsonify(dijkstra(edges, start, target))
    if algo == "prim":
        return jsonify(prim_mst(edges))
    if algo == "kruskal":
        return jsonify(kruskal_mst(edges))
    if algo == "bipartite":
        return jsonify(is_bipartite(edges))
    if algo == "ford":
        return jsonify(ford_fulkerson(edges, start, target))
    if algo == "fleury":
        return jsonify(fleury_algorithm(edges))
    if algo == "hierholzer":
        return jsonify(hierholzer_algorithm(edges))

    return jsonify({"error": "Thuật toán không tồn tại"}), 400

# ================= CONVERT =================

@app.route("/api/convert/adjlist", methods=["POST"])
def to_adj_list():
    edges = parse_edge_list(request.json.get("edge_text", ""))
    return jsonify(edges_to_adj_list(edges))

@app.route("/api/convert/matrix", methods=["POST"])
def to_matrix():
    edges = parse_edge_list(request.json.get("edge_text", ""))
    return jsonify(edges_to_adj_matrix(edges))

if __name__ == "__main__":
    app.run(debug=True)
