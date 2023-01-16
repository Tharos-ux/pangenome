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
                # Link
                elif datas[0] == 'L':
                    if keep_tags:
                        gfa_writer.write(
                            '\n'+'\t'.join([datas[0], sub('\D', '', datas[1]), datas[2], sub('\D', '', datas[3])]+datas[4:]))
                    else:
                        gfa_writer.write(
                            '\n'+'\t'.join([datas[0], sub('\D', '', datas[1]), datas[2], sub('\D', '', datas[3]), datas[4], datas[5]]))
                    # datas[5] == cigar
                    link_informations.append(
                        (sub('\D', '', datas[1])+datas[2], sub('\D', '', datas[3])+datas[4], datas[5]))
                # We don't really know linetype
                else:
                    gfa_writer.write('\n'+'\t'.join(datas))
        if p_lines:
            # We need to add P-lines at this point
            visited_paths: list = []
            for (edge_a, edge_b, cigar_left) in link_informations:
                for (edge_c, edge_d, cigar_right) in link_informations:
                    if (edge_a, edge_b) != (edge_c, edge_d) and edge_b == edge_c:
                        # We found a chain
                        if find_bool_subpath(f"{edge_a},{edge_b},{edge_d}", visited_paths):
                            # If a-X-b is not already written in any path
                            suffixes_positions: list = find_suffix(
                                f"{edge_a},{edge_c}", visited_paths)
                            prefixes_positions: list = find_prefix(
                                f"{edge_b},{edge_d}", visited_paths)
                            # Lookup for suffixes & prefixes
                            if len(suffixes_positions) > 0:
                                for pos in suffixes_positions:
                                    visited_paths[pos] = (
                                        f"{visited_paths[pos][0]},{edge_d}", f"{visited_paths[pos][1]},{cigar_right}")
                            elif len(prefixes_positions) > 0:
                                for pos in prefixes_positions:
                                    visited_paths[pos] = (
                                        f"{edge_a},{visited_paths[pos][0]}", f"{cigar_left},{visited_paths[pos][1]}")
                            else:
                                # De-novo path
                                visited_paths += [
                                    (f"{edge_a},{edge_b},{edge_d}", f"{cigar_left},{cigar_right}")]
            # Cleaning subsequences
            paths_to_keep: list = []
            for (path, cigars) in visited_paths:
                if find_bool_subpath(path, paths_to_keep):
                    paths_to_keep, status = chain(path, cigars, paths_to_keep)
                    if not status:
                        paths_to_keep.append((path, cigars))

                    # Writing P-lines
            for path_number, (line, cigar) in enumerate(paths_to_keep):
                gfa_writer.write(
                    f"\nP\t{path_number+number_of_nodes}\t{line}\t{cigar}")


def chain(path: str, cigar: str, list_of_paths: list) -> tuple:
    """Given a duet of string and a list of tuples, looks if the first half of the tuple is a prefix or a suffix of sequence, and merges it if so

    Args:
        path (str): the string we look for a prefix or suffix
        cigar (str): tags associated to the string
        list_of_paths (list): the list we search into

    Returns:
        tuple: (updated list, bool if a change was made)
    """
    changed_state = False
    for i, (p, c) in enumerate(list_of_paths):
        if p.split(',')[-1] == path.split(',')[0]:
            # current path is the suffix of loop path
            list_of_paths[i] = (
                f"{p},{','.join(path.split(',')[1:])}", f"{c},{','.join(cigar.split(',')[1:])}")
            changed_state = True
        elif p.split(',')[0] == path.split(',')[-1]:
            # current path is the prefix of loop path
            list_of_paths[i] = (
                f"{','.join(path.split(',')[:-1])},{p}", f"{','.join(cigar.split(',')[:-1])},{c}")
            changed_state = True
    return list_of_paths, changed_state


def find_bool_subpath(path: str, list_of_paths: list) -> bool:
    """Given a string and a list of string, returns if path is not a substring of list of strings.

    Args:
        path (str): a path we want to find
        list_of_paths (list): a path where we may find our subpath

    Returns:
        bool: if sequence is NOT subsequence of any, or equal
    """
    return not any([True for (p, _) in list_of_paths if path in p])


def find_suffix(path: str, list_of_paths: list) -> list:
    """Given a string and a list of strings, returns positions of list where string is a suffix

    Args:
        path (str): sequence we look for
        list_of_paths (list): table we look into

    Returns:
        list: positions of occurences
    """
    a, b = path.split(',')
    return [i for i, (p, _) in enumerate(list_of_paths) if p.split(',')[-2] == a and p.split(',')[-1] == b]


def find_prefix(path: str, list_of_paths: list) -> list:
    """Given a string and a list of strings, returns positions of list where string is a suffix

    Args:
        path (str): sequence we look for
        list_of_paths (list): table we look into

    Returns:
        list: positions of occurences
    """
    a, b = path.split(',')
    return [i for i, (p, _) in enumerate(list_of_paths) if p.split(',')[0] == a and p.split(',')[1] == b]


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
