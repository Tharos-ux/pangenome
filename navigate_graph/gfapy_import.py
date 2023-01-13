"Loading rGFA files"
from argparse import ArgumentParser
from gfapy import Gfa


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="gfa-like file")
    args = parser.parse_args()

    gfa_graph: Gfa = Gfa.from_file(args.file, dialect="standard")  # rgfa

    # print(gfa_graph.dovetails)
    print(gfa_graph.segment_names)
