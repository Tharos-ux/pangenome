"Test implem odgi"
from sys import path
from os.path import exists
from os import system
from argparse import ArgumentParser

odgi_path: str = "./.env/bin"
if exists(odgi_path):
    path.append(odgi_path)
    import odgi
else:
    exit(1)


def convert_graph(gfa_file: str) -> str | None:
    """_summary_

    Args:
        gfa_file (str): _description_
    """
    if not exists(f"{gfa_file.split('.')[0]}.og"):
        system(f"odgi build -g {gfa_file} -o {gfa_file.split('.')[0]}.og")
    return f"{gfa_file.split('.')[0]}.og"


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="gfa-like file")
    args = parser.parse_args()

    og_file = convert_graph(gfa_file=args.file)

    if og_file is None:  # guard
        exit()

    g = odgi.graph()
    g.load(og_file)
    print(
        f"Sucessfully loaded file containing {g.get_node_count()} nodes and {g.get_path_count()} paths.")
    """
    path = g.get_path_handle('1600')
    step = g.path_begin(path)
    while (g.has_next_step(step)):
        # get the node handle from the step handle
        current_node_handle = g.get_handle_of_step(step)
        # ask the node handle for the sequence
        print(g.get_sequence(current_node_handle))
        # progress to the next step
        step = g.get_next_step(step)
    current_node_handle = g.get_handle_of_step(step)
    print(g.get_sequence(current_node_handle))
    """
