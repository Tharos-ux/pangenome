"Plots graph statistics"
from re import sub
from collections import Counter
from argparse import ArgumentParser, SUPPRESS
from statsmodels.stats.weightstats import DescrStatsW
from networkx import MultiDiGraph, is_isolate
import matplotlib.pyplot as plt
from grapher import init_graph


def size_ratio(counts: list, threshold: int) -> float:
    """Computes the ratio of nodes below or equal a threshold / nodes above a threshold
    1 means all nodes are above threshold

    Args:
        graph (MultiDiGraph): _description_
        threshold (int): _description_

    Returns:
        float: _description_
    """
    num, denom = .0, .0
    for size, count in counts:
        if size <= threshold:
            num += count
        else:
            denom += count
    return num/(denom+num)


def plot_ratio(counts: list, names: list, x_min: int, x_max: int, x_step: int = 1) -> None:
    plt.figure(figsize=(20, 4))
    for i, count in enumerate(counts):
        ratios: list = [size_ratio(count, x)
                        for x in range(x_min, x_max, x_step)]
        plt.plot(ratios, label=names[i])
    plt.xscale('log')
    plt.legend(loc='upper center', bbox_to_anchor=(
        0.5, -0.05), ncol=len(counts))
    plt.ylim(0.5, 1)
    plt.xlim(1, x_max)
    plt.savefig('test.png', bbox_inches='tight')
    plt.show()


def lonely_nodes(graph: MultiDiGraph) -> list:
    """Those are some of the saddest nodes. :(

    Args:
        graph (MultiDiGraph): _description_

    Returns:
        list: _description_
    """
    return sorted(
        [(k, v) for k, v in Counter(
            [
                int(sub('\D', '', datas['title'])) for node, datas in graph.nodes(data=True)
                if is_isolate(graph, node)
            ]
        ).items()]
    )


def neighboured_nodes(graph: MultiDiGraph) -> list:
    """Those are not lonely.

    Args:
        graph (MultiDiGraph): _description_

    Returns:
        list: _description_
    """
    return sorted(
        [(k, v) for k, v in Counter(
            [
                int(sub('\D', '', datas['title'])) for node, datas in graph.nodes(data=True)
                if not is_isolate(graph, node)
            ]
        ).items()]
    )


def parse_gfa(input_file: str) -> list:
    """Counts the length distribution of all segments in a gfa file

    Args:
        input_file (str): path to a GFA-like file

    Returns:
        Counter: length distribution of sequences
    """
    with open(input_file, 'r', encoding='utf-8') as gfa_reader:
        return sorted([(k, v) for k, v in Counter([len(seq.split()[2]) for seq in gfa_reader if seq.split()[0] == 'S']).items()])


def plot_distribution(counts: list[list[tuple]], lonely: list[list[tuple]] | None, graph_names: list) -> None:
    """Given a Counter of length distribution, plots ths distribution

    Args:
        counts (list): list of sorted Counter, length distribution of segments of graph
    """
    fig, axs = plt.subplots(nrows=len(counts), ncols=1,
                            sharex=True, figsize=(10, 12))
    for i in range(len(counts)):
        x: list = [k for (k, _) in counts[i]]
        y: list = [v for (_, v) in counts[i]]
        w_stats: DescrStatsW = DescrStatsW(x, weights=y, ddof=0)
        if lonely is not None:
            a: list = [k for (k, _) in lonely[i]]
            b: list = [v for (_, v) in lonely[i]]
        try:
            axs[i].set_title(
                f"Distribution for {graph_names[i]}, |V|={sum(y)}, $\mu$={round(w_stats.mean,ndigits=2)}, $\sigma$={round(w_stats.std,ndigits=2)}")
            axs[i].plot(x, y)
            axs[i].plot(a, b)
            axs[i].set_yscale('log')
        except TypeError:
            axs.set_title(
                f"Distribution for {graph_names[i]}, |V|={sum(y)}, $\mu$={round(w_stats.mean,ndigits=2)}, $\sigma$={round(w_stats.std,ndigits=2)}")
            axs.plot(x, y)
            axs.plot(a, b)
            axs.set_yscale('log')
    try:
        for ax in axs.flat:
            ax.set(xlabel='Sequence size', ylabel='Number of occurences')
            ax.label_outer()
    except AttributeError:
        axs.set(xlabel='Sequence size', ylabel='Number of occurences')
    plt.xscale('log')
    fig.savefig('test.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="gfa-like file", nargs='+')
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Plot distribution of node length across graph')
    parser.add_argument(
        "-g",
        "--gfa_version",
        help="Tells the GFA input style",
        required=True,
        choices=['rGFA', 'GFA1', 'GFA1.1', 'GFA1.2', 'GFA2']
    )
    args = parser.parse_args()

    counters: list = [parse_gfa(filepath) for filepath in args.file] if isinstance(
        args.file, list) else [parse_gfa(args.file)]
    names: list = [filepath.split('.')[0].split('/')[-1] for filepath in args.file] if isinstance(
        args.file, list) else [args.file.split('.')[0].split('/')[-1]]
    # plot_distribution(counters, names)

    lengths: list = [parse_gfa(name) for name in args.file]
    # max_len: int = min([length[-1][0] for length in lengths])

    plot_ratio(lengths, names, 0, 10000, 1)
