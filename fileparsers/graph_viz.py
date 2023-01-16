"GFA file vizualizer"
from argparse import ArgumentParser, SUPPRESS
from pyvis.network import Network
from networkx import Graph, DiGraph, MultiDiGraph
from mycolorpy import colorlist
from PIL import Image
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.pyplot import subplots, savefig, plot, legend, figure
from re import sub
from random import randrange


def render_graph(gfa_file: str, debug: bool = False) -> None:
    """Creates a interactive .html file representing the given graph

    Args:
        gfa_file (str): path to a rGFA file
        debug (bool, optional): plots less nodes in graph. Defaults to False.
    """
    # S are nodes and L are edges
    alignment_length: list = [len(l.split()[2]) for l in open(
        gfa_file, "r", encoding="utf-8") if l.split()[0] == "S"]
    maximum_alignment: int = max(alignment_length)
    alignment_length: list = [l/maximum_alignment for l in alignment_length]
    # Creating a colormap
    colors: list = colorlist.gen_color_normalized(
        cmap="viridis", data_arr=alignment_length)
    paths: list = [l.split() for l in open(
        gfa_file, "r", encoding="utf-8") if l.split()[0] == "P"]
    number_paths: int = len(paths)
    colors_paths: list = colorlist.gen_color_normalized(
        cmap="copper", data_arr=[i/number_paths for i in range(number_paths)])

    # Creating the colorbar for legend
    fig, ax = subplots(1, 1)
    norm = Normalize(vmin=0, vmax=maximum_alignment)
    ax.figure.colorbar(
        cm.ScalarMappable(norm=norm, cmap="viridis"),
        ax=ax, pad=.05, extend='both', fraction=1)
    ax.axis('off')
    savefig(f"{gfa_file.split('.')[0]}_cbar.png", bbox_inches='tight')

    Image.open(f"{gfa_file.split('.')[0]}_cbar.png").rotate(
        90, Image.NEAREST, expand=True).save(f"{gfa_file.split('.')[0]}_cbar.png")

    # Get all alignment sources
    alignment_sources: set = set([int(l.split()[6][5:]) for l in open(
        gfa_file, "r", encoding="utf-8") if l.split()[0] == "L"])
    max_source: int = max(alignment_sources)
    normalized_sources: list = [s/max_source for s in alignment_sources]
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
    fig.savefig(
        f"{gfa_file.split('.')[0]}_legend.png", dpi="figure", bbox_inches=bbox)

    graph = MultiDiGraph()

    i: int = 0
    j: int = 0
    k: int = 0
    with open(gfa_file, "r", encoding="utf-8") as reader:
        for line in reader:
            if line[0] == "S" and ((debug and i < 10) or not debug):
                graph.add_node(sub('\D', '', line.split()[1]), size=4+(16*alignment_length[i]), color=my_cmap[int(line.split()[6][5:])],
                               title=f"Seq. length:{len(line.split()[2])}\n"+'\n'.join(line.split()[3:]))

                i += 1
            if line[0] == "L" and ((debug and j < 10) or not debug):

                if int(line.split()[6][5:]) == 0:  # From reference sequence
                    graph.add_edge(line.split()[1],
                                   line.split()[3], color=my_cmap[int(line.split()[6][5:])], weight=3, label=f"{line.split()[2]}/{line.split()[4]}")
                else:
                    graph.add_edge(line.split()[1],
                                   line.split()[3], color=my_cmap[int(line.split()[6][5:])], weight=1.5, label=f"{line.split()[2]}/{line.split()[4]}")
                j += 1
            if line[0] == "P" and ((debug and k < 10) or not debug):
                color: int = randrange(len(colors_paths))
                path_to_incorporate: list = [
                    sub('\D', '', data) for data in line.split()[2].split(',')]
                node_duets_of_path: list = [
                    (path_to_incorporate[pos], path_to_incorporate[pos+1]) for pos in range(len(path_to_incorporate)-1)]
                for (node_a, node_b) in node_duets_of_path:
                    graph.add_edge(
                        node_a, node_b, color=colors_paths[color], weight=0.5, arrows='?', label=line.split()[1])
                colors_paths.pop(color)
                k += 1

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
    args = parser.parse_args()

    render_graph(gfa_file=args.file, debug=args.debug)
