"Computes and print the length of each sequence in a fasta file"
from argparse import ArgumentParser, SUPPRESS
from Bio import SeqIO


def show_assemblies_size(fasta_file: str) -> None:
    """Show the size of each element inside a fasta file

    Args:
        fasta_file (str): a path to a fasta like file
    """
    print(f">>> {fasta_file}")
    for fasta in SeqIO.parse(open(fasta_file, encoding="utf-8"), 'fasta'):
        print(f"{fasta.id} -> {len(fasta.seq)} bases long")


def compare_fasta_sequences(fasta_files: list):
    fastas: list = []
    for fasta_file in fasta_files:
        fastas.append([(fasta.id, fasta.seq) for fasta in SeqIO.parse(
            open(fasta_file, encoding="utf-8"), 'fasta')])
    for fasta_id, seq in fastas[0]:
        if all([seq.strip() == x.strip() for fasta in fastas for id, x in fasta if fasta_id == id]):
            print(f"Sequence for {fasta_id} is identical across all files.")
        else:
            print(f"Sequence for {fasta_id} is different !")


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="fasta-like file", nargs='+')
    args = parser.parse_args()
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Calculates the length of all sequences in file.')

    for file in args.file:
        show_assemblies_size(fasta_file=file)

    compare_fasta_sequences(args.file)
