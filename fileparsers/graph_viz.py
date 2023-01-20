"GFA file vizualizer"
from argparse import ArgumentParser, SUPPRESS
from random import randrange
from re import sub
from pyvis.network import Network
from networkx import MultiDiGraph, add_path
from mycolorpy import colorlist
from PIL import Image
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.pyplot import subplots, savefig, plot, legend, figure
from collections import Counter
try:
    from fileparsers.gfatypes import LineType, Record, GfaStyle
except ModuleNotFoundError:
    from gfatypes import LineType, Record, GfaStyle


def assert_format(gfa_file: str, gfa_version: GfaStyle) -> LineType:
    """By checking the first letter of each line, we check which lines can help us to create edges

    Args:
        gfa_file (str): filepath to GFA
        gfa_version (GfaStyle): the assumed-by-user GFA subformat

    Returns:
        LineType: the line type we should get paths from
    """
    is_present: dict = {line_type: False for line_type in LineType}
    with open(gfa_file, "r", encoding="utf-8") as reader:
        for line in reader:
            is_present[LineType(line[0])] = True

    if gfa_version == GfaStyle.RGFA:
        return LineType.SEGMENT
    if is_present[LineType.WALK]:
        return LineType.WALK
    elif is_present[LineType.PATH]:
        return LineType.PATH


def standalone_graph(gfa_file: str, gfa_version: str) -> MultiDiGraph:
    graph = MultiDiGraph()

    line_counts: Counter = Counter({t.name: 0 for t in LineType})
    with open(gfa_file, "r", encoding="utf-8") as reader:
        for line in reader:
            gfa_line: Record = Record(line, gfa_version)
            match (gfa_line.linetype, gfa_line.gfastyle):
                case (LineType.SEGMENT, _):
                    graph.add_node(
                        gfa_line.line.name,
                        title=f"Seq. length: {gfa_line.line.length}"
                    )
                case (LineType.LINE, _):
                    graph.add_edge(
                        gfa_line.line.start,
                        gfa_line.line.end,
                        label=gfa_line.line.orientation
                    )
                case (LineType.WALK, GfaStyle.GFA1_1):
                    for (a, b) in gfa_line.line.walk:
                        if not graph.has_edge(a, b):
                            graph.add_edge(
                                a,
                                b,
                                color=my_cmap[gfa_line.line.origin],
                                weight=2,
                            )
                case (LineType.PATH, GfaStyle.RGFA):
                    raise ValueError
                case (LineType.PATH, _):
                    add_path(graph, sum(
                        ([a, b] for ((a, _), (b, _)) in gfa_line.line.walk)))

            line_counts[gfa_line.linetype] += 1
    return graph


def compute_graph(gfa_file: str, gfa_version: str, plines: bool = False, save_legend: bool = False) -> MultiDiGraph:
    """_summary_

    Args:
        gfa_file (str): _description_
        gfa_version (str): _description_
        plines (bool, optional): _description_. Defaults to False.
        save_legend (bool, optional): _description_. Defaults to False.

    Returns:
        MultiDiGraph: _description_
    """
    # We need to check what the graph contains first, even if we specify version, because each software has its own particularities
    _v: GfaStyle = GfaStyle(gfa_version)
    _t: LineType = assert_format(gfa_file, _v)

    # S are nodes and L are edges
    alignment_length: list = [len(l.split()[2]) for l in open(
        gfa_file, "r", encoding="utf-8") if l.split()[0] == "S"]
    maximum_alignment: int = max(alignment_length)
    alignment_length: list = [l/maximum_alignment for l in alignment_length]
    # Creating a colormap
    colors_paths: list = []
    if plines:
        paths: list = [l.split() for l in open(
            gfa_file, "r", encoding="utf-8") if l.split()[0] == "P"]
        number_paths: int = len(paths)
        colors_paths: list = colorlist.gen_color_normalized(
            cmap="copper", data_arr=[i/number_paths for i in range(number_paths)])

    # Get all alignment sources

    if _v == GfaStyle.RGFA:
        alignment_sources: set = set([l.split()[6][5:] for l in open(
            gfa_file, "r", encoding="utf-8") if l.split()[0] == "L"])
    elif _v == GfaStyle.GFA1_1:
        alignment_sources: set = set([l.split()[2] for l in open(
            gfa_file, "r", encoding="utf-8") if l.split()[0] == "W"])
    elif _v == GfaStyle.GFA1:
        alignment_sources: set = set([l.split()[1] for l in open(
            gfa_file, "r", encoding="utf-8") if l.split()[0] == "P"])
    else:
        raise NotImplementedError()

    max_source: int = len(alignment_sources)
    normalized_sources: list = [i/(max_source+1)
                                for i in range(len(alignment_sources)+1)]
    colors_sources: list = colorlist.gen_color_normalized(
        cmap="rainbow", data_arr=normalized_sources)
    my_cmap: dict = {source: colors_sources[i]
                     for i, source in enumerate(alignment_sources)}
    figure().clear()
    # Creating the legends for alignments
    handles = [plot([], [], marker="s", color=cs, ls="none")[0]
               for cs in colors_sources]
    l = legend(handles, alignment_sources, loc=3,
               framealpha=1, frameon=False)
    fig = l.figure  # type: ignore
    bbox = l.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    if save_legend:
        fig.savefig(
            f"{gfa_file.split('.')[0]}_legend.png", dpi="figure", bbox_inches=bbox)

    graph = MultiDiGraph()

    line_counts: Counter = Counter({t.name: 0 for t in LineType})
    with open(gfa_file, "r", encoding="utf-8") as reader:
        for line in reader:
            gfa_line: Record = Record(line, gfa_version)
            match (gfa_line.linetype, gfa_line.gfastyle):
                case (LineType.SEGMENT, GfaStyle.RGFA):
                    graph.add_node(
                        gfa_line.line.name,
                        size=4 +
                        (16*alignment_length[line_counts[LineType.SEGMENT]]),
                        color=my_cmap[gfa_line.line.origin],
                        title=f"Seq. length: {gfa_line.line.length}"
                    )
                case (LineType.SEGMENT, _):
                    graph.add_node(
                        gfa_line.line.name,
                        size=4 +
                        (16*alignment_length[line_counts[LineType.SEGMENT]]),
                        title=f"Length: {gfa_line.line.length}"
                    )
                case (LineType.LINE, GfaStyle.RGFA):
                    if gfa_line.line.origin == 0:  # reference sequence
                        graph.add_edge(
                            gfa_line.line.start,
                            gfa_line.line.end,
                            color=my_cmap[gfa_line.line.origin],
                            weight=3,
                            label=gfa_line.line.orientation
                        )
                    else:
                        graph.add_edge(
                            gfa_line.line.start,
                            gfa_line.line.end,
                            color=my_cmap[gfa_line.line.origin],
                            weight=1.5,
                            label=gfa_line.line.orientation
                        )
                case (LineType.WALK, GfaStyle.GFA1_1):
                    for (a, b) in gfa_line.line.walk:
                        if not graph.has_edge(a, b):
                            graph.add_edge(
                                a,
                                b,
                                color=my_cmap[gfa_line.line.origin],
                                weight=2,
                            )
                case (LineType.PATH, GfaStyle.RGFA):
                    if plines:
                        color: int = randrange(len(colors_paths))
                        path_to_incorporate: list = [
                            sub('\D', '', data) for data in line.split()[2].split(',')]
                        node_duets_of_path: list = [
                            (path_to_incorporate[pos], path_to_incorporate[pos+1]) for pos in range(len(path_to_incorporate)-1)]
                        for (node_a, node_b) in node_duets_of_path:
                            graph.add_edge(
                                node_a, node_b, color=colors_paths[color], weight=0.5, arrows='?', label=line.split()[1])
                        colors_paths.pop(color)
                case (LineType.PATH, GfaStyle.GFA1):
                    for ((a, o_a), (b, o_b)) in gfa_line.line.path:
                        if not graph.has_edge(a, b):
                            graph.add_edge(
                                a,
                                b,
                                color=my_cmap[gfa_line.line.name],
                                weight=2,
                                label=f"{o_a}/{o_b}"
                            )

            line_counts[gfa_line.linetype] += 1
    return graph


def render_graph(gfa_file: str, debug: bool = False, plines: bool = False, gfa_version: str = 'rGFA') -> None:
    """Creates a interactive .html file representing the given graph

    Args:
        gfa_file (str): path to a rGFA file
        debug (bool, optional): plots less nodes in graph. Defaults to False.
        plines (bool, optional) : plots the P-lines as paths on the graph. Defaults to False.
    """
    graph: MultiDiGraph = compute_graph(
        gfa_file, gfa_version, save_legend=True)

    graph_visualizer = Network(
        height='1000px', width='100%', directed=True)
    graph_visualizer.toggle_physics(True)
    graph_visualizer.from_nx(graph)
    graph_visualizer.set_edge_smooth('dynamic')
    try:
        graph_visualizer.show(f"{gfa_file.split('.')[0]}_graph.html")
    except FileNotFoundError:
        # Path indicated for file may not be correct regarding the lib but writes .html anyways, so ignore ^^
        pass

    with open(f"{gfa_file.split('.')[0]}_graph.html", "r", encoding="utf-8") as html_reader:
        outfile = html_reader.readlines()
        # <img src='{gfa_file.split('.')[0].split('/')[-1]}_cbar.png' align='center' rotate='90'>
    outfile[10] = f"<h1>Graph for <b>{gfa_file.split('.')[0].split('/')[-1]}</b><img src='{gfa_file.split('.')[0].split('/')[-1]}_legend.png' align='center'></h1>"
    with open(f"{gfa_file.split('.')[0]}_graph.html", "w", encoding="utf-8") as html_writer:
        html_writer.writelines(outfile)


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="gfa-like file")
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Plot a interactive html graph given a rGFA file.')
    parser.add_argument(
        "-d", "--debug", help="Plot less nodes in order to create a toy file", action='store_true')
    parser.add_argument(
        "-p", "--p_lines", help="Shows P-lines as secondary paths", action='store_true')
    parser.add_argument(
        "-g", "--gfa_version", help="Tells the GFA input style", required=True, choices=['rGFA', 'GFA1', 'GFA1.1', 'GFA1.2', 'GFA2'])
    args = parser.parse_args()

    render_graph(
        gfa_file=args.file,
        debug=args.debug,
        plines=args.p_lines,
        gfa_version=args.gfa_version
    )
