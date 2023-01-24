"Creates a graph we can navigate in."
from argparse import ArgumentParser, SUPPRESS
from networkx import MultiDiGraph, add_path, isolates
from mycolorpy import colorlist
try:
    from fileparsers.gfatypes import LineType, Record, GfaStyle
except ModuleNotFoundError:
    from gfatypes import LineType, Record, GfaStyle


def init_graph(gfa_file: str, gfa_version: str, n_aligns: int) -> MultiDiGraph:
    """Initializes the graph without displaying it

    Args:
        gfa_file (str): GFA-like input file
        gfa_version (str): user-assumed GFA subversion
        n_aligns (int): number of distinct origin sequences

    Raises:
        ValueError: Occurs if graph specified format isn't correct given the file
        NitImplementedError : Occurs if the function is currently not impelemented yet

    Returns:
        MultiDiGraph: a graph representing the given pangenome
    """
    graph = MultiDiGraph()

    cmap: list = colorlist.gen_color_normalized(
        cmap="rainbow", data_arr=[i/n_aligns for i in range(n_aligns)])

    visited_paths: int = 0
    version: GfaStyle = GfaStyle(gfa_version)
    with open(gfa_file, "r", encoding="utf-8") as reader:
        for line in reader:
            gfa_line: Record = Record(line, gfa_version)
            match (gfa_line.linetype, version):
                case LineType.SEGMENT, _:
                    graph.add_node(
                        gfa_line.line.name,
                        title=f"{gfa_line.line.length} bp."
                    )
                case LineType.WALK, _:
                    if not gfa_line.line.idf == '_MINIGRAPH_':
                        add_path(
                            graph,
                            [node for (node, _) in gfa_line.line.walk],
                            title=gfa_line.line.name,
                            color=cmap[visited_paths]
                        )
                        visited_paths += 1
                case LineType.PATH, _:
                    add_path(
                        graph,
                        [node for (node, _) in gfa_line.line.path],
                        title=gfa_line.line.name,
                        color=cmap[visited_paths]
                    )
                    visited_paths += 1
                case LineType.LINE, GfaStyle.RGFA:
                    graph.add_edge(
                        gfa_line.line.start,
                        gfa_line.line.end,
                        title=str(gfa_line.line.origin),
                        color=cmap[gfa_line.line.origin]
                    )
    graph.remove_nodes_from(list(isolates(graph)))
    return graph


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="gfa-like file")
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Returns a MultiDiGraph object.')
    parser.add_argument(
        "-n", "--number_alignments", help="Gives the number of origin sequences", required=True, type=int)
    parser.add_argument(
        "-g", "--gfa_version", help="Tells the GFA input style", required=True, choices=['rGFA', 'GFA1', 'GFA1.1', 'GFA1.2', 'GFA2'])
    args = parser.parse_args()

    pangenome_graph: MultiDiGraph = init_graph(
        gfa_file=args.file,
        gfa_version=args.gfa_version,
        n_aligns=args.number_alignments
    )
