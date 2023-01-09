"Parses GFA files"
from argparse import ArgumentParser


class GfaGraph:

    def __init__(self, gfa_file: str):
        self.__file = gfa_file
        with open(self.__file, "r", encoding="utf-8") as gfa_reader:
            for i, line in enumerate(gfa_reader):
                if line.split()[0] == 'S':
                    setattr(self, line.split()[1], line.split()[3:]+[i])

    def request_sequence(self, target: str) -> str:
        target_line: int = getattr(self, target)[-1]
        with open(self.__file, "r", encoding="utf-8") as gfa_reader:
            for i, line in enumerate(gfa_reader):
                if i == target_line:
                    return line.split()[2]


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("file", type=str, help="gfa-like file")
    args = parser.parse_args()
