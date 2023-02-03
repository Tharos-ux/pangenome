"Isolates from tags from fasta file"
from argparse import ArgumentParser, SUPPRESS
from json import dump
from os import remove, path
from Bio import SeqIO


def export_mapping(paf_file: str, save: bool = False, threshold: int = 4000000) -> list:
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
            if int(l.split()[10]) >= threshold
        ],
        key=lambda x: x['sequence_length']
    )[::-1]

    if save:
        dump(mapping, open(
            f"{paf_file.split('.')[0]}_out.json", "w", encoding="utf-8"))
    datas = {}
    for mapd in mapping:
        datas[mapd['query_seq_name']] = datas[mapd['query_seq_name']] + \
            mapd['sequence_length']if mapd['query_seq_name'] in datas else mapd['sequence_length']

    print('\n'.join([f"{name} > {length}" for name, length in datas.items()]))
    return mapping


if __name__ == "__main__":

    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="paf-like file")
    args = parser.parse_args()

    export_mapping(args.file, True)
