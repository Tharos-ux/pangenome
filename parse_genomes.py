"Isolates from tags from fasta file"
from argparse import ArgumentParser
from Bio import SeqIO


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "file", type=str, help="fasta-like file")
    args = parser.parse_args()

    # id du chromosome que l'on veut isoler
    chromosome: str = "3"

    # contient les codes de retour ; seul 1 est valide
    x: list[int] = [SeqIO.write(fasta, f"{args.file}_chr{chromosome}.fasta", 'fasta') for fasta in SeqIO.parse(
        open(args.file, encoding="utf-8"), 'fasta') if fasta.id == chromosome]

    print(f"For chromosome {chromosome}, {len(x)} sequences were isolated.")
