"Isolates from tags from fasta file"
from argparse import ArgumentParser, SUPPRESS
from json import dump
from Bio import SeqIO
from os import remove


def export_mapping(paf_file: str, save: bool = False) -> list:
    """Exports a list of dicts

    Args:
        paf_file (str): path to a paf-formated file
        save (bool, optional): if should save to disk. Defaults to False.

    Returns:
        list: dicts containing for each scaffold mapping between query and reference
    """
    mapping: list[dict] = sorted(
        [
            {
                'query_seq_name': l.split()[0],
                'ref_seq_name':l.split()[5],
                'sequence_length':int(l.split()[10])
            }
            for l in open(paf_file, "r", encoding="utf-8")
            if int(l.split()[10]) >= 4000000
        ],
        key=lambda x: x['sequence_length']
    )[::-1]

    if save:
        dump(mapping, open(
            f"{paf_file.split('.')[0]}_out.json", "w", encoding="utf-8"))
    return mapping


def isolate_scaffolds(fasta_file: str, paf_file: str, chromosom: str) -> None:
    """Isolate scaffolds based upon correspondances from reference to query

    Args:
        fasta_file (str): query file
        paf_file (str): mapping of reference against query
        chromosom (str): chromosom identifier, name used on reference file
    """
    remove(f"{fasta_file}_chr{chromosom}.fasta")
    with open(f"{fasta_file}_chr{chromosom}.fasta", 'a', encoding="utf-8") as handler:
        retcodes: list[int] = [
            SeqIO.write(
                fasta, handler, 'fasta'
            )
            for fasta in SeqIO.parse(
                open(fasta_file, 'r', encoding="utf-8"), 'fasta'
            )
            if fasta.id in
            [
                x['query_seq_name'] for x in export_mapping(paf_file=paf_file, save=False) if x['ref_seq_name'] == chromosom
            ]
        ]

    if not all(retcodes):
        print(f"For chromosom {chromosom}, parsing failed.")
    else:
        print(
            f"For chromosom {chromosom}, {len(retcodes)} sequences were isolated.")


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument(
        "file", type=str, help="fasta-like file")
    parser.add_argument(
        "paffile", type=str, help="paf-like file")
    parser.add_argument(
        "chromosom", type=str, help="name of assembly on reference sequence")
    args = parser.parse_args()
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Extracts from a fasta-like file all sequences in a query assembly given a mapping to a reference and an identifier on reference.')

    isolate_scaffolds(fasta_file=args.file,
                      paf_file=args.paffile, chromosom=args.chromosom)
