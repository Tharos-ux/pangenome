from argparse import ArgumentParser, SUPPRESS
from networkx import number_of_isolates, number_of_edges, number_of_nodes
from fileparsers import init_graph, html_graph, plot_distribution, lonely_nodes, neighboured_nodes

if __name__ == '__main__':

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="gfa-like file", nargs='+')
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Plot distribution of node length across graph')
    parser.add_argument(
        "-g", "--gfa_version", help="Tells the GFA input style", required=True, choices=['rGFA', 'GFA1', 'GFA1.1', 'GFA1.2', 'GFA2'])
    args = parser.parse_args()

    for i, file in enumerate(args.file):
        g = init_graph(file, args.gfa_version, 3)
        html_graph(g, f'test_{i}')

    """
    graphs = [compute_graph(file, args.gfa_version) for file in args.file]
    for graph in graphs:
        print(f"Graph has {number_of_isolates(graph)} lonely nodes for a total of {number_of_nodes(graph)} nodes, and {number_of_edges(graph)} edges.")
    counters: list = [neighboured_nodes(g) for g in graphs]
    lonely: list = [lonely_nodes(g) for g in graphs]
    for i, counter in enumerate(counters):
        print(
            f"Neighboured nodes : {sum([k for (k,_) in counter])}/{sum([v for (_,v) in counter])} || Lonely nodes : {sum([k for (k,_) in lonely[i]])}/{sum([v for (_,v) in lonely[i]])}")

    names: list = [filepath.split('.')[0].split('/')[-1]
                   for filepath in args.file]
    plot_distribution(counters, lonely, names)
    """
