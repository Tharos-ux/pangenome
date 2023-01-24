"Converts various GFA files"
from argparse import ArgumentParser, SUPPRESS
from re import sub


def rgfa_to_gfa(input_file: str, output_file: str, p_lines: bool = False, keep_tags: bool = False) -> None:
    """Converts rGFA (minigraph) to GFA1 files by adding header and P-lines
    This process is not lossless !!! We lost tags in-between.

    Args:
        input_file (str): a path to a rGFA file
        output_file (str): a path where file should be written
    """
    # Cleaning file
    edgelist: list = []
    number_of_nodes: int = 1
    with open(output_file, "w", encoding="utf-8") as gfa_writer:
        pass
    link_informations: list = []
    with open(output_file, "a", encoding="utf-8") as gfa_writer:
        # Header
        gfa_writer.write("H\tVN:Z:1.0")
        with open(input_file, "r", encoding="utf-8") as gfa_reader:
            for line in gfa_reader:
                datas: list = line.split()
                # Segment
                if datas[0] == 'S':
                    number_of_nodes += 1
                    if keep_tags:
                        gfa_writer.write(
                            '\n'+'\t'.join([datas[0], sub('\D', '', datas[1])]+datas[2:]))
                    else:
                        gfa_writer.write(
                            '\n'+'\t'.join([datas[0], sub('\D', '', datas[1]), datas[2]]))
                # Line
                elif datas[0] == 'L':
                    if keep_tags:
                        gfa_writer.write(
                            '\n'+'\t'.join([datas[0], sub('\D', '', datas[1]), datas[2], sub('\D', '', datas[3])]+datas[4:]))
                    else:
                        gfa_writer.write(
                            '\n'+'\t'.join([datas[0], sub('\D', '', datas[1]), datas[2], sub('\D', '', datas[3]), datas[4], datas[5]]))
                    # datas[5] == cigar
                    # datas[6][5:] == origin_sequence
                    link_informations.append(
                        (sub('\D', '', datas[1])+datas[2], sub('\D', '', datas[3])+datas[4], datas[5], datas[6][5:]))
                    edgelist.append((sub('\D', '', datas[1]), [], sub(
                        '\D', '', datas[3]), int(datas[6][5:])))
                # We don't really know linetype
                else:
                    gfa_writer.write('\n'+'\t'.join(datas))

        print(len(create_p_lines(edgelist)))
        if p_lines:
            # We need to add P-lines at this point
            visited_paths: list = []
            for (edge_a, edge_b, cigar_left, origin_seq_alpha) in link_informations:
                for (edge_c, edge_d, cigar_right, origin_seq_beta) in link_informations:
                    if (edge_a, edge_b) != (edge_c, edge_d) and edge_b == edge_c and origin_seq_beta == origin_seq_alpha:
                        # We found a chain
                        if find_bool_subpath(f"{edge_a},{edge_b},{edge_d}", origin_seq_alpha, visited_paths):
                            # If a-X-b is not already written in any path
                            suffixes_positions: list = find_suffix(
                                f"{edge_a},{edge_c}",
                                origin_seq_alpha,
                                visited_paths
                            )
                            prefixes_positions: list = find_prefix(
                                f"{edge_b},{edge_d}",
                                origin_seq_alpha,
                                visited_paths
                            )
                            # Lookup for suffixes & prefixes
                            if len(suffixes_positions) > 0:
                                for pos in suffixes_positions:
                                    visited_paths[pos] = (
                                        f"{visited_paths[pos][0]},{edge_d}",
                                        f"{visited_paths[pos][1]},{cigar_right}",
                                        visited_paths[pos][2]
                                    )
                            elif len(prefixes_positions) > 0:
                                for pos in prefixes_positions:
                                    visited_paths[pos] = (
                                        f"{edge_a},{visited_paths[pos][0]}",
                                        f"{cigar_left},{visited_paths[pos][1]}",
                                        visited_paths[pos][2]
                                    )
                            else:
                                # De-novo path
                                visited_paths += [
                                    (f"{edge_a},{edge_b},{edge_d}", f"{cigar_left},{cigar_right}", origin_seq_alpha)]
            # Cleaning subsequences
            paths_to_keep: list = []
            for (path, cigars, origin) in visited_paths:
                if find_bool_subpath(path, origin, paths_to_keep):
                    paths_to_keep, chained = deep_chains(
                        path, cigars, origin, paths_to_keep, 3)
                    if not chained:
                        paths_to_keep.append((path, cigars, origin))

            # assembling subpaths
            diff: int = 0
            reference: str = paths_to_keep[0][0]
            complete_paths: list = [
                (paths_to_keep[0][0], '*', paths_to_keep[0][2])]
            paths_to_keep: list = paths_to_keep[1:]
            while diff != len(paths_to_keep) and len(paths_to_keep) > 0:
                diff = len(paths_to_keep)
                try:
                    paths_to_keep: list = min_distance(
                        paths_to_keep[0][0],
                        paths_to_keep[0][2],
                        reference,
                        paths_to_keep[1:]
                    )
                except ValueError:
                    complete_paths.append(
                        (paths_to_keep[0][0], '*', paths_to_keep[0][2]))
                    paths_to_keep = paths_to_keep[1:]

            # Writing P-lines
            for path_number, (line, cigar, origin) in enumerate(complete_paths):
                gfa_writer.write(
                    f"\nP\t{path_number+number_of_nodes}\t{line}\t{cigar}\tSR:i:{origin}")


def create_p_lines(edges: list[tuple]) -> list:
    """Assuming edges is a four-part tuple list [(edge-a,middle|[],edge-b,sequence-of-edge)] computes the reconstruction of genomes.

    Args:
        edges (list[tuple]): edge description
    """
    # Edges in reference are shared.
    bank_of_edges: list[tuple] = [(start, stop, seq)
                                  for (start, stop, seq) in edges if seq == 0]

    # We iterate until convergence, which happens when no sequence could be merged
    while True:
        match iterate_edges(edges, bank_of_edges):
            case None:
                return edges
            case (new_edge, pos_to_edit, pos_to_suppress):
                edges[pos_to_edit] = new_edge
                edges.pop(pos_to_suppress)


def iterate_edges(edges: list[tuple], bank_of_edges: list[tuple]) -> tuple | None:
    """_summary_

    Args:
        edges (list[tuple]): _description_
        bank_of_edges (list[tuple]): _description_

    Returns:
        tuple: _description_
    """
    for edge_a in edges:
        for edge_b in edges + bank_of_edges:
            if edge_a != edge_b:
                match (edge_a, edge_b):
                    case ((start, internal_left, bridge_a, seq_a), (bridge_b, internal_right, end, seq_b)) | ((bridge_a, internal_right, end, seq_a), (start, internal_left, bridge_b, seq_b)) if seq_a == seq_b and bridge_a == bridge_b:
                        # Same seq and chained, or same seq and chained and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq_a)
                    case ((start, internal_left, bridge_a, 0), (bridge_b, internal_right, end, seq)) | ((start, internal_left, bridge_a, seq), (bridge_b, internal_right, end, 0)) | ((bridge_a, internal_right, end, 0), (start, internal_left, bridge_b, seq)) | ((bridge_a, internal_right, end, seq), (start, internal_left, bridge_b, 0)) if bridge_a == bridge_b:
                        # Different seq but chained to ref, or different seq but chained to ref and reversed
                        return (start, internal_left + [bridge_a] + internal_right, end, seq)
                    case _:
                        # No edge can be merge
                        return


def deep_chains(path: str, cigar: str, origin: str, list_of_paths: list, max_depth: int) -> tuple:
    """Given a duet of string and a list of tuples, looks if the first half of the tuple is a prefix or a suffix of sequence, and merges it if so

    Args:
        path (str): the string we look for a prefix or suffix
        cigar (str): tags associated to the string
        origin (str) : the origin sequence of the 'path'
        list_of_paths (list): the list we search into
        max_depth (int): gives the maximum number of segments we have to compare (depth>0)

    Returns:
        tuple: (updated list, bool if a change was made)
    """
    for i, (p, c, o) in enumerate(list_of_paths):
        if o == origin:
            query: list = path.split(',')
            ref: list = p.split(',')
            for depth in range(1, max_depth+1):
                if all([query[r] == ref[r-depth] for r in range(depth)]):
                    # current path is the suffix of loop path
                    list_of_paths[i] = (
                        f"{p},{','.join(path.split(',')[depth:])}",
                        f"{c},{','.join(cigar.split(',')[depth:])}",
                        origin
                    )
                    return list_of_paths, True
                elif all([ref[r] == query[r-depth] for r in range(depth)]):
                    # current path is the prefix of loop path
                    list_of_paths[i] = (
                        f"{','.join(path.split(',')[:-1])},{p}",
                        f"{','.join(cigar.split(',')[:-1])},{c}",
                        origin
                    )
                    return list_of_paths, True
    return list_of_paths, False


def min_distance(path: str, origin: str, reference_path: str, list_of_unclassified: list):
    """_summary_

    Args:
        path (list): _description_
        reference_path (list): _description_
        list_of_unclassified (list): _description_
    """
    path: list = path.split(',')
    seek_ref = reference_path.replace('-', '+').split(',')
    reference_path: list = reference_path.split(',')

    idx_start_path: int = seek_ref.index(path[0])
    idx_end_path: int = seek_ref.index(path[-1])
    distances: list = [
        abs(
            idx_start_path-seek_ref.index(query.split(',')[0][-1])
        ) for query, _, o in list_of_unclassified if o == origin
    ]

    target: int = distances.index(min(distances))
    query_seq: list = list_of_unclassified[target][0].split(',')

    idx_start_query: int = seek_ref.index(query_seq[0])
    idx_end_query: int = seek_ref.index(query_seq[-1])

    if idx_start_path > idx_start_query:
        # path is located after query
        list_of_unclassified[target] = (','.join(
            query_seq +
            reference_path[idx_end_query: idx_start_path] +
            path), '*', origin
        )
    else:
        list_of_unclassified[target] = (','.join(
            path +
            reference_path[idx_end_path:idx_start_query] +
            query_seq), '*', origin
        )

    return list_of_unclassified


def find_bool_subpath(path: str, origin: str, list_of_paths: list) -> bool:
    """Given a string and a list of string, returns if path is not a substring of list of strings.

    Args:
        path (str): a path we want to find
        origin (str) : the origin sequence of the path
        list_of_paths (list): a path where we may find our subpath

    Returns:
        bool: if sequence is NOT subsequence of any, or equal
    """
    return not any([path in p and o == origin for (p, _, o) in list_of_paths])


def find_suffix(path: str, origin: str, list_of_paths: list) -> list:
    """Given a string and a list of strings, returns positions of list where string is a suffix

    Args:
        path (str): sequence we look for
        origin (str) : the origin sequence of the path
        list_of_paths (list): table we look into

    Returns:
        list: positions of occurences
    """
    a, b = path.split(',')
    return [i for i, (p, _, o) in enumerate(list_of_paths) if p.split(',')[-2] == a and p.split(',')[-1] == b and origin == o]


def find_prefix(path: str, origin: str, list_of_paths: list) -> list:
    """Given a string and a list of strings, returns positions of list where string is a suffix

    Args:
        path (str): sequence we look for
        origin (str) : the origin sequence of the path
        list_of_paths (list): table we look into

    Returns:
        list: positions of occurences
    """
    a, b = path.split(',')
    return [i for i, (p, _, o) in enumerate(list_of_paths) if p.split(',')[0] == a and p.split(',')[1] == b and origin == o]


def subsampling_rgfa(input_file: str, output_file: str, nodes: list, keep_tags: bool = True) -> None:
    """From an input rGFA file, extracts lines corresponding to the subgraph within the list of nodes

    Args:
        input_file (str): input rGFA
        output_file (str): output rGFA
        nodes (list): all nodes we should keep
        keep_tags (bool, optional): if rGFA-specific should be in output file. Defaults to True.
    """
    nodes_to_keep: list = [sub('\D', '', node) for node in nodes]
    nodes_names: list = [i+1 for i in range(len(nodes_to_keep))]
    with open(output_file, "w", encoding="utf-8") as gfa_writer:
        pass
    with open(output_file, "a", encoding="utf-8") as gfa_writer:
        with open(input_file, "r", encoding="utf-8") as gfa_reader:
            for line in gfa_reader:
                datas: list = line.split()
                # Segment
                if datas[0] == 'S' and sub('\D', '', datas[1]) in nodes_to_keep:
                    if keep_tags:
                        gfa_writer.write(
                            '\t'.join([datas[0], str(nodes_names[nodes_to_keep.index(sub('\D', '', datas[1]))])]+datas[2:])+'\n')
                    else:
                        gfa_writer.write(
                            '\t'.join([datas[0], str(nodes_names[nodes_to_keep.index(sub('\D', '', datas[1]))])]+[datas[2]])+'\n')
                # Link
                elif datas[0] == 'L' and sub('\D', '', datas[1]) in nodes_to_keep and sub('\D', '', datas[3]) in nodes_to_keep:
                    if keep_tags:
                        gfa_writer.write(
                            '\t'.join([datas[0], str(nodes_names[nodes_to_keep.index(sub('\D', '', datas[1]))]),
                                      datas[2], str(nodes_names[nodes_to_keep.index(sub('\D', '', datas[3]))])] + datas[4:]) + '\n')
                    else:
                        gfa_writer.write(
                            '\t'.join([datas[0], str(nodes_names[nodes_to_keep.index(sub('\D', '', datas[1]))]),
                                      datas[2], str(nodes_names[nodes_to_keep.index(sub('\D', '', datas[3]))])] + [datas[4]]) + '\n')


def reconstruct_fasta(input_file: str, output_file: str, paths_lists: list[list], paths_names: list) -> None:
    """_summary_

    Args:
        input_file (str): _description_
        output_file (str): _description_
        paths_lists (list[list]): _description_
        paths_names (list): _description_
    """
    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            if line.split()[0] == 'S':
                for i, path in enumerate(paths_lists):
                    try:
                        paths_lists[i][path.index(sub('\D', '', line.split()[1]))] = line.split()[
                            2].strip()
                    except ValueError:
                        pass
    for i, seq in enumerate(paths_lists):
        with open(f"{paths_names[i]}{output_file}", 'w', encoding='utf-8') as outfile:
            outfile.write(f">{paths_names[i]}\n{''.join(seq)}")


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="rGFA file")
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='This script aims to convert rGFA files issued from minigraph to GFA1 compatible format. It implies to rename nodes and add P-lines if asked for.')
    parser.add_argument(
        "-p", "--plines", help="Asks to calculate p-lines for graph", action='store_true')
    parser.add_argument(
        "-k", "--keep", help="Keeps rGFA-specific tags in output", action='store_true')
    args = parser.parse_args()

    rgfa_to_gfa(
        args.file, f"{args.file.split('.')[0]}_gfa1.gfa", p_lines=args.plines, keep_tags=args.keep)
