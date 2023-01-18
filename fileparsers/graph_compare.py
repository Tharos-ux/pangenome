"Plots graph statistics"
from scipy.interpolate import UnivariateSpline
from collections import Counter
from numpy import linspace, average
from argparse import ArgumentParser, SUPPRESS
from statsmodels.stats.weightstats import DescrStatsW
import matplotlib.pyplot as plt


def parse_gfa(input_file: str) -> list:
    """Counts the length distribution of all segments in a gfa file

    Args:
        input_file (str): path to a GFA-like file

    Returns:
        Counter: length distribution of sequences
    """
    with open(input_file, 'r', encoding='utf-8') as gfa_reader:
        return sorted([(k, v) for k, v in Counter([len(seq.split()[2]) for seq in gfa_reader if seq.split()[0] == 'S']).items()])


def plot_distribution(counts: list[list[tuple]], graph_names: list) -> None:
    """Given a Counter of length distribution, plots ths distribution

    Args:
        counts (list): list of sorted Counter, length distribution of segments of graph
    """
    fig, axs = plt.subplots(nrows=len(counts), ncols=1,
                            sharex=True, figsize=(10, 12))
    for i in range(len(counts)):
        x: list = [k for (k, _) in counts[i]]
        # max_length = max(x)
        y: list = [v for (_, v) in counts[i]]
        w_stats: DescrStatsW = DescrStatsW(x, weights=y, ddof=0)
        # max_height = max(y)
        # spl = UnivariateSpline(x, y)
        # xs = linspace(1, max_length, max_height)
        axs[i].set_title(
            f"Distribution for {graph_names[i]}, |V|={sum(y)}, $\mu$={round(w_stats.mean,ndigits=2)}, $\sigma$={round(w_stats.std,ndigits=2)}")
        axs[i].plot(x, y)
        # axs[i].plot(xs, spl(xs))
        axs[i].set_yscale('log')
    plt.xscale('log')
    for ax in axs.flat:
        ax.set(xlabel='Sequence size', ylabel='Number of occurences')
        ax.label_outer()
    fig.savefig('test.png', bbox_inches='tight')
    plt.show()


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="gfa-like file", nargs='+')
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Plot distribution of node length across graph')
    args = parser.parse_args()

    counters: list = [parse_gfa(filepath) for filepath in args.file] if isinstance(
        args.file, list) else [parse_gfa(args.file)]
    names: list = [filepath.split('.')[0].split('/')[-1] for filepath in args.file] if isinstance(
        args.file, list) else [args.file.split('.')[0].split('/')[-1]]
    plot_distribution(counters, names)
