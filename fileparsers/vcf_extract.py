'Extract sequences given a graph to a VCF'
from argparse import ArgumentParser, SUPPRESS
from re import sub
from gfa_types import LineType, Record, GfaStyle


def grab_paths(gfa_file: str, gfa_version: str) -> list[Record]:
    """From a given gfa-like file, grabs the path of each haplotype

    Args:
        gfa_file (str): a path to a gfa-like file
        gfa_version (str): a GFA-format identifier

    Raises:
        NotImplementedError: in case of rGFA which is currently not supportef

    Returns:
        list[Record]: list of paths, one for each haplotype
    """
    paths: list[Record] = []
    version: GfaStyle = GfaStyle(gfa_version)
    with open(gfa_file, "r", encoding="utf-8") as reader:
        for line in reader:
            gfa_line: Record = Record(line, gfa_version)
            match (gfa_line.linetype, version):
                case LineType.WALK, _:
                    if not gfa_line.line.idf == '_MINIGRAPH_':  # type:ignore
                        paths.append(gfa_line)
                case LineType.PATH, _:
                    paths.append(gfa_line)
                case LineType.LINE, GfaStyle.RGFA:
                    raise NotImplementedError('rGFA currently not supported')
                case _:
                    pass
    return paths


def extract_variants(paths: list[Record], reference: str) -> list:
    "Given a set of paths, seeks variations"

    return []


def node_topology(gfa_line: str) -> dict:
    """Tries to extract offset from line"""
    if gfa_line[0] != 'S':
        raise ValueError("Line is not a node.")
    datas = gfa_line.split()
    length: int = len(datas[2])
    offset: int | None = None
    origin: int | None = None
    for data in datas[2:]:
        if data[:2] == 'SO':
            offset = int(sub('\D', '', data))
        elif data[:2] == 'SR':
            origin = int(sub('\D', '', data))
    return {'length': length, 'offset': offset, 'end_pos': length+offset if offset is not None else None, 'sequence': origin}


def node_offset(target_node: str, paths: list[Record]) -> int:
    for path in paths:
        for (node, orientation) in path.line.path:
            if target_node == node:

                if orientation ==


def revcomp(string: str, compl: dict = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}) -> str:
    try:
        return ''.join([compl[s] for s in string][::-1])
    except IndexError as exc:
        raise IndexError(
            "Complementarity does not include all chars in sequence.") from exc


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Reconstruct VCF from a GFA graph')
    parser.add_argument("file", type=str, help="gfa-like file")
    args = parser.parse_args()

    with open(args.file, 'r', encoding='utf-8') as gfa_reader:
        for line in gfa_reader:
            if line[0] == 'S':
                print(node_topology(line))
