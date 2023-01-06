"Isolates from tags from fasta file"
from argparse import ArgumentParser
from Bio import SeqIO


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "file", type=str, help="fasta-like file")
    parser.add_argument(
        "paffile", type=str, help="paf-like file")
    parser.add_argument(
        "chromosom", type=str, help="name of assembly on reference sequence")
    args = parser.parse_args()

    mapping: list[dict] = sorted(
        [
            {
                'query_seq_name': l.split()[0],
                'ref_seq_name':l.split()[5],
                'residue_match_number':int(l.split()[10])
            }
            for l in open(args.paffile, "r", encoding="utf-8")
            if int(l.split()[10]) >= 4000000
        ],
        key=lambda x: x['residue_match_number']
    )[::-1]

    querries_to_keep: list = [x['query_seq_name']
                              for x in mapping if x['ref_seq_name'] == args.chromosom]

    # contient les codes de retour ; seul 1 est valide
    x: list[int] = [SeqIO.write(fasta, f"{args.file}_chr{args.chromosom}.fasta", 'fasta') for fasta in SeqIO.parse(
        open(args.file, encoding="utf-8"), 'fasta') if fasta.id in querries_to_keep]

    print(
        f"For chromosome {args.chromosom}, {len(x)} sequences were isolated.")
