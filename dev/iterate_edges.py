def iterate_edges(edges: list[tuple]) -> tuple | None:
    """Iterates over the edges and chains them

    Args:
        edges (list[tuple]): a list of all edges inside the graph
        bank_of_edges (list[tuple]): a list of all edges from the reference inside the graph

    Returns:
        tuple: (new_edge,position_to_edit,position_to_del)
    """
    for i, edge_a in enumerate(edges):
        for j, edge_b in enumerate(edges):
            if edge_a != edge_b:
                match (edge_a, edge_b):
                    case ((start, internal_left, bridge_a, seq_a), (bridge_b, internal_right, end, seq_b)) | ((bridge_a, internal_right, end, seq_a), (start, internal_left, bridge_b, seq_b)) if seq_a == seq_b and bridge_a == bridge_b and end not in [start]+internal_left:
                        # Same seq and chained, or same seq and chained and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq_a), i, j
                    case ((start, internal_left, bridge_a, 0), (bridge_b, internal_right, end, seq)) if bridge_a == bridge_b and seq != 0 and end not in [start]+internal_left:
                        # Different seq but chained to ref, or different seq but chained to ref and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq), j, float('inf')
                    case ((start, internal_left, bridge_a, seq), (bridge_b, internal_right, end, 0)) if bridge_a == bridge_b and seq != 0 and end not in [start]+internal_left:
                        # Different seq but chained to ref, or different seq but chained to ref and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq), i, float('inf')
                    case ((bridge_a, internal_right, end, 0), (start, internal_left, bridge_b, seq)) if bridge_a == bridge_b and seq != 0 and end not in [start]+internal_left:
                        # Different seq but chained to ref, or different seq but chained to ref and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq), j, float('inf')
                    case ((bridge_a, internal_right, end, seq), (start, internal_left, bridge_b, 0)) if bridge_a == bridge_b and seq != 0 and end not in [start]+internal_left:
                        # Different seq but chained to ref, or different seq but chained to ref and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq), i, float('inf')
                    case _:
                        # No edge can be merge
                        pass
