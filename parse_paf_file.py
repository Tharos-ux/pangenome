"Mapping from paf file"
from argparse import ArgumentParser
from json import dump
from collections import Counter


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument(
        "file", type=str, help="paf-like file")
    args = parser.parse_args()

    mapping: list[dict] = sorted(
        [
            {
                'query_seq_name': l.split()[0],
                'ref_seq_name':l.split()[5],
                'residue_match_number':int(l.split()[10])
            }
            for l in open(args.file, "r", encoding="utf-8")
            if int(l.split()[10]) >= 4000000
        ],
        key=lambda x: x['residue_match_number']
    )[::-1]

    print("\nMATCHES")
    print('\n'.join([f"Chromosome {k} : {v} hits" for k, v in Counter(
        [x['query_seq_name'] for x in mapping if x['query_seq_name'] == x['ref_seq_name']]).items()]))

    print("\nMISSMATCHES")
    print('\n'.join(
        [f"{x['query_seq_name']} against {x['ref_seq_name']}" for x in mapping if x['query_seq_name'] != x['ref_seq_name']]))

    dump(mapping, open(f"{args.file}_out.json", "w", encoding="utf-8"))
