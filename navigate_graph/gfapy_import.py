"Loading rGFA files"
from argparse import ArgumentParser
from gfapy import Gfa


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="gfa-like file")
    args = parser.parse_args()

    gfa_graph: Gfa = Gfa.from_file(args.file, dialect="standard")  # rgfa

    # some_segment = gfa_graph.segment_names[3]
    # print(some_segment)
    print(gfa_graph.edges)
    # print(gfa_graph.is_cut_segment(gfa_graph.line(some_segment)))
    # print(gfa_graph.segment_connected_component("4"))
