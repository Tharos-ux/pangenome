"Isolates tags from fasta file"
from argparse import ArgumentParser


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "file", type=str, help="fasta-like file")
    args = parser.parse_args()

    with open(f"{args.file}_out.txt", "w", encoding="utf-8") as writer:
        writer.write(
            '\n'.join([l for l in open(args.file, "r", encoding="utf-8") if l[0] == '>']))
