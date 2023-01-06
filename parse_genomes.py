"Isolates from tags from fasta file"
from argparse import ArgumentParser
from Bio import SeqIO


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "file", type=str, help="fasta-like file")
    args = parser.parse_args()

    # id du chromosome que l'on veut isoler
    chromosome: list = ["h1tg000002l", "h1tg000087l", "h1tg000071l"]

    # contient les codes de retour ; seul 1 est valide
    x: list[int] = [SeqIO.write(fasta, f"{args.file}_chr{chromosome}.fasta", 'fasta') for fasta in SeqIO.parse(
        open(args.file, encoding="utf-8"), 'fasta') if fasta.id in chromosome]

    print(f"For chromosome {chromosome}, {len(x)} sequences were isolated.")
