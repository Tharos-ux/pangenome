"Computes and print the length of each sequence in a fasta file"
from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO


def show_assemblies_size(fasta_file: str) -> None:
    """Show the size of each element inside a fasta file

    Args:
        fasta_file (str): a path to a fasta like file
    """
    for fasta in SeqIO.parse(open(fasta_file, encoding="utf-8"), 'fasta'):
        print(f"{fasta.id} -> {fasta.seq} bases long")


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "file", type=str, help="fasta-like file")
    args = parser.parse_args()
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Calculates the length of all sequences in file.')

    show_assemblies_size(fasta_file=args.file)
