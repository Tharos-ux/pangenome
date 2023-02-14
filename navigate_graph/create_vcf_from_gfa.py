"Aims to create a VCF file form a GFA one."
from argparse import ArgumentParser, SUPPRESS
from json import loads


def grab_gfa_datas(gfa_file: str) -> dict:
    gfa_datas: dict = dict()
    with open(gfa_file, 'r', encoding='utf-8') as gfa_reader:
        for line in gfa_reader:
            if line.startswith('S'):
                datas: list = line.split('\t')
                print([x for x in datas if x.startswith('PO:J:')][0][5:])
                gfa_datas[datas[1]] = loads(
                    [x for x in datas if x.startswith('PO:J:')][0][5:])
    return gfa_datas


if __name__ == '__main__':
    parser = ArgumentParser(add_help=False)
    parser.add_argument("file", type=str, help="Path to a gfa-like file")
    parser.add_argument('-h', '--help', action='help', default=SUPPRESS,
                        help='Creates a VCF from a GFA file')
    args = parser.parse_args()

    print(grab_gfa_datas(args.file))
