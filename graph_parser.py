"GFA file vizualizer"
from argparse import ArgumentParser
from pyvis.network import Network
from networkx import Graph
from mycolorpy import colorlist
from PIL import Image
from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.pyplot import subplots, savefig, plot, legend, figure

if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="gfa-like file")
    parser.add_argument(
        "-d", "--debug", help="Plot less nodes in order to create a toy file", action='store_true')
    args = parser.parse_args()

    # S are nodes and L are edges
    alignment_length: list = [len(l.split()[2]) for l in open(
        args.file, "r", encoding="utf-8") if l.split()[0] == "S"]
    maximum_alignment: int = max(alignment_length)
    alignment_length: list = [l/maximum_alignment for l in alignment_length]
    # Creating a colormap
    colors: list = colorlist.gen_color_normalized(
        cmap="viridis", data_arr=alignment_length)

    # Creating the colorbar for legend
    fig, ax = subplots(1, 1)
    norm = Normalize(vmin=0, vmax=maximum_alignment)
    cbar = ax.figure.colorbar(
        cm.ScalarMappable(norm=norm, cmap="viridis"),
        ax=ax, pad=.05, extend='both', fraction=1)
    ax.axis('off')
    savefig(f"{args.file.split('.')[0]}_cbar.png", bbox_inches='tight')

    Image.open(f"{args.file.split('.')[0]}_cbar.png").rotate(
        90, Image.NEAREST, expand=True).save(f"{args.file.split('.')[0]}_cbar.png")

    # Get all alignment sources
    alignment_sources: set = set([int(l.split()[6][5:]) for l in open(
        args.file, "r", encoding="utf-8") if l.split()[0] == "L"])
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
        f"{args.file.split('.')[0]}_legend.png", dpi="figure", bbox_inches=bbox)

    graph = Graph()

    i: int = 0
    j: int = 0
    with open(args.file, "r", encoding="utf-8") as reader:
        for line in reader:
            if line[0] == "S" and ((args.debug and i < 10) or not args.debug):
                graph.add_node(line.split()[1], size=4+(16*alignment_length[i]), color=colors[i],
                               title=f"Seq. length:{len(line.split()[2])}\n"+'\n'.join(line.split()[3:]))
                i += 1
            if line[0] == "L" and ((args.debug and j < 10) or not args.debug):
                if int(line.split()[6][5:]) == 0:  # From reference sequence
                    graph.add_edge(line.split()[1],
                                   line.split()[3], color=my_cmap[int(line.split()[6][5:])], weight=2)
                else:
                    graph.add_edge(line.split()[1],
                                   line.split()[3], color=my_cmap[int(line.split()[6][5:])], weight=0.5)
                j += 1

    # if I want to draw a .png not interactive figure
    # plt.figure().clear()
    # nx.draw(graph, node_size=3, with_labels=False, node_color='red')
    # plt.savefig(f"{args.file.split('.')[0]}_graph.html")

    graph_visualizer = Network(
        height='900px', width='100%')  # heading=f"Graph for {args.file.split('.')[0].split('/')[-1]}"
    # graph_visualizer.show_buttons()
    graph_visualizer.toggle_physics(not args.debug)
    graph_visualizer.from_nx(graph)
    try:
        graph_visualizer.show(f"{args.file.split('.')[0]}_graph.html")
    except FileNotFoundError:
        # Path indicated for file may not be correct regarding the lib but writes .html anyways, so ignore
        pass

    with open(f"{args.file.split('.')[0]}_graph.html", "r", encoding="utf-8") as html_reader:
        outfile = html_reader.readlines()
    outfile[10] = f"<h1>Graph for <b>{args.file.split('.')[0].split('/')[-1]}</b></h1><img src='{args.file.split('.')[0].split('/')[-1]}_cbar.png' align='center' rotate='90'>\n<img src='{args.file.split('.')[0].split('/')[-1]}_legend.png' align='center'>"
    with open(f"{args.file.split('.')[0]}_graph.html", "w", encoding="utf-8") as html_writer:
        html_writer.writelines(outfile)
