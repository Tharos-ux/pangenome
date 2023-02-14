from gfatypes import Record


def follow_path(path: Record, nodes_length: list) -> list:
    cumsum: list = list(range(len(path.line.path)))
    cumsum[0] = nodes_length[int(path.line.path[0][0])]
    for i, (node_name, _) in enumerate(path.line.path[1:]):
        cumsum[i] = nodes_length[int(node_name)] + cumsum[i-1]


def get_positions(list_of_paths: list[Record]) ->
