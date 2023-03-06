from networkx import MultiDiGraph, add_path, all_simple_paths


def topology(paths: dict[str, list], reference: str) -> None:
    candidates: int = 1
    pinch: int = len(paths)*2
    graph: MultiDiGraph = MultiDiGraph()
    for nodes in paths.values():
        add_path(graph, nodes)
    query_length: int = len(paths[reference])
    for i, node in enumerate(paths[reference]):
        deg: int = graph.degree[node]
        if deg == pinch:
            candidates += 1
        elif i == 0 or i == query_length-1:
            if deg == pinch/2:
                candidates += 1
    print(f"Encountered bubbles : {candidates//2}")


"""
inside_paths = all_simple_paths(
    graph, source=paths[reference][id], target=paths[reference][id+1])
inside_nodes = {
    node for path in inside_paths for node in path}

if (n_nodes := len(inside_nodes)) == 1:
    print("Simple bubble, IN/DEL")
elif n_nodes == 2:
    print("Simple bubble, SUB")
elif n_nodes > 2:
    print("Superbubble!")
"""

graph_paths: dict = {
    "BtChar1": "1>2>4>5>6>7>8>9>10>11>12", "BtChar2": "1>3>4>5>7>9>10>12", "SeqBt1": "1>2>4>5>6>7>9>10>11>12"
}

graph_paths = {path: val.replace('<', '>').split('>')
               for path, val in graph_paths.items()}

print(graph_paths)

topology(graph_paths, 'SeqBt1')

"""
from gfagraphs import Graph,Segment

snapshot:dict = {}

def topological_sort(graph:Graph):
    def recursive_topological_sort(graph:Graph,vertex:Segment):
        vertex.datas['visited'] = True
        

    order:int = len(graph.segments)
    for vertex in graph.segments:
        vertex.datas['visited'] = False
    source:Segment = graph.segments[0]
    recursive_topological_sort(graph,source)

"""
